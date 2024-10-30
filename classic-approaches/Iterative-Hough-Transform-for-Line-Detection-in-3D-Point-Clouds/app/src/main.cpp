
#include <filesystem>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <open3d/Open3D.h>
#include "../libs/eigen-3.4.0/Eigen/Dense"
#include "../libs/hough3d/vector3d.h"
#include "../libs/hough3d/pointcloud.h"
#include "../libs/hough3d/hough.h"

using Eigen::MatrixXf;

double orthogonal_LSQ(const PointCloud &pc, Vector3d *a, Vector3d *b)
{
    double rc = 0.0;

    // anchor point is mean value
    *a = pc.meanValue();

    // copy points to libeigen matrix
    Eigen::MatrixXf points = Eigen::MatrixXf::Constant(pc.points.size(), 3, 0);
    for (int i = 0; i < points.rows(); i++)
    {
        points(i, 0) = pc.points.at(i).x;
        points(i, 1) = pc.points.at(i).y;
        points(i, 2) = pc.points.at(i).z;
    }

    // compute scatter matrix ...
    MatrixXf centered = points.rowwise() - points.colwise().mean();
    MatrixXf scatter = (centered.adjoint() * centered);

    // ... and its eigenvalues and eigenvectors
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXf> eig(scatter);
    Eigen::MatrixXf eigvecs = eig.eigenvectors();

    // we need eigenvector to largest eigenvalue
    // libeigen yields it as LAST column
    b->x = eigvecs(0, 2);
    b->y = eigvecs(1, 2);
    b->z = eigvecs(2, 2);
    rc = eig.eigenvalues()(2);

    return (rc);
}

std::vector<std::string> split(const std::string &str, char delimiter)
{
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;

    while (std::getline(ss, token, delimiter))
    {
        tokens.push_back(token);
    }
    return tokens;
}

void print(std::string message)
{
    std::cout << message << std::endl;
}

int main()
{
    // Display point cloud
    std::filesystem::path input_file_path = std::filesystem::current_path() / "app" / "testdata.dat";
    std::ifstream file(input_file_path);

    std::vector<Eigen::Vector3d> points;

    if (file.is_open())
    {
        std::string line;
        while (std::getline(file, line))
        {
            std::istringstream ss(line);
            std::string token;
            double x, y, z;

            std::getline(ss, token);

            // if stars with "#", skip
            if (token[0] == '#')
            {
                continue;
            }

            std::vector<std::string> point_array = split(token, ',');

            x = std::stod(point_array[0]);
            y = std::stod(point_array[1]);
            z = std::stod(point_array[2]);
            points.emplace_back(x, y, z);
        }
        file.close();
    }
    else
    {
        std::cerr << "Nie można otworzyć pliku: " << input_file_path << std::endl;
        return -1;
    }

    auto cloud = std::make_shared<open3d::geometry::PointCloud>();
    for (const auto &point : points)
    {
        cloud->points_.push_back(point);
    }

    print(std::to_string(cloud->points_.size()));

    open3d::visualization::Visualizer visualizer;
    visualizer.CreateVisualizerWindow("PointCloud", 800, 600, 100, 100, open3d::visualization::Visualizer::Headless);

    // Dodaj chmurę punktów do sceny
    visualizer.AddGeometry(cloud);

    // Ustawienie widoku kamery (opcjonalnie, aby dostosować widok)
    visualizer.GetViewControl().SetLookat({0, 0, 0});
    visualizer.GetViewControl().SetUp({0, 1, 0});
    visualizer.GetViewControl().SetFront({0, 0, -1});
    visualizer.GetViewControl().SetZoom(0.8);

    // Zapisz renderowaną scenę jako obraz bez wyświetlania okna
    visualizer.PollEvents();
    visualizer.UpdateRender();
    visualizer.CaptureScreenImage("screenshot.png");

    // Zakończ wizualizator
    visualizer.DestroyVisualizerWindow();

    return 0;

    double opt_dx = 0.0;
    int opt_nlines = 0;
    int opt_minvotes = 0;

    // enum Outformat
    // {
    //     format_normal,
    //     format_gnuplot,
    //     format_raw
    // };
    // Outformat opt_outformat = format_normal;
    // int opt_verbose = 0;
    // char *infile_name = NULL;
    // char *outfile_name = NULL;

    // number of icosahedron subdivisions for direction discretization
    int granularity = 4;
    int num_directions[7] = {12, 21, 81, 321, 1281, 5121, 20481};

    // bounding box of point cloud
    Vector3d minP, maxP, minPshifted, maxPshifted;

    // diagonal length of point cloud
    double d;

    std::filesystem::path current_path = std::filesystem::current_path();
    auto outfile_path = current_path / "app" / "output.dat";
    print(outfile_path);
    auto outfile = fopen(outfile_path.c_str(), "w");
    // if (!outfile)
    // {
    //     fprintf(stderr, "Error: cannot open outfile '%s'!\n", outfile_name);
    //     return 1;
    // }

    PointCloud X;
    print("Reading from file...");
    int status = X.readFromFile(input_file_path.c_str());

    if (status != 0)
    {
        print("Error: cannot open infile 'testdata.dat'!");
        return 1;
    }

    print("Amount of points in point cloud: " + std::to_string(X.points.size()));

    // center cloud and compute new bounding box
    X.getMinMax3D(&minP, &maxP);
    d = (maxP - minP).norm();
    if (d == 0.0)
    {
        fprintf(stderr, "Error: all points in point cloud identical\n");
        return 1;
    }
    X.shiftToOrigin();
    X.getMinMax3D(&minPshifted, &maxPshifted);

    // estimate size of Hough space
    if (opt_dx == 0.0)
    {
        opt_dx = d / 64.0;
    }
    else if (opt_dx >= d)
    {
        fprintf(stderr, "Error: dx too large\n");
        return 1;
    }

    double num_x = floor(d / opt_dx + 0.5);
    double num_cells = num_x * num_x * num_directions[granularity];
    printf("info: x'y' value range is %f in %.0f steps of width dx=%f\n", d, num_x, opt_dx);
    printf("info: Hough space has %.0f cells taking %.2f MB memory space\n", num_cells, num_cells * sizeof(unsigned int) / 1000000.0);

    // first Hough transform
    Hough *hough;
    try
    {
        hough = new Hough(minPshifted, maxPshifted, opt_dx, granularity);
    }
    catch (const std::exception &e)
    {
        fprintf(stderr, "Error: cannot allocate memory for %.0f Hough cells"
                        " (%.2f MB)\n",
                num_cells,
                (double(num_cells) / 1000000.0) * sizeof(unsigned int));
        return 2;
    }
    hough->add(X);

    // iterative Hough transform
    // (Algorithm 1 in IPOL paper)
    PointCloud Y; // points close to line
    double rc;
    unsigned int nvotes;
    int nlines = 0;
    print("Starting iterative Hough transform...");
    do
    {

        Vector3d a; // anchor point of line
        Vector3d b; // direction of line

        hough->subtract(Y); // do it here to save one call

        nvotes = hough->getLine(&a, &b);
        // if (opt_verbose > 1)
        // {
        //     Vector3d p = a + X.shift;
        //     printf("info: highest number of Hough votes is %i for the following "
        //            "line:\ninfo: a=(%f,%f,%f), b=(%f,%f,%f)\n",
        //            nvotes, p.x, p.y, p.z, b.x, b.y, b.z);
        // }

        X.pointsCloseToLine(a, b, opt_dx, &Y);

        rc = orthogonal_LSQ(Y, &a, &b);

        print("1->" + std::to_string(X.points.size()));
        print("2->" + std::to_string(Y.points.size()));
        print("3->" + std::to_string(opt_dx));
        print("3->" + std::to_string(rc));

        if (rc == 0.0)
        {
            break;
        }

        X.pointsCloseToLine(a, b, opt_dx, &Y);
        nvotes = Y.points.size();
        if (nvotes < (unsigned int)opt_minvotes)
            break;

        rc = orthogonal_LSQ(Y, &a, &b);
        if (rc == 0.0)
        {
            break;
        }

        a = a + X.shift;

        nlines++;

        print("---");
        print(std::to_string(Y.points.size()));
        print(std::to_string(opt_nlines));
        print(std::to_string(nlines));
        print("---");

        fprintf(outfile, "%f %f %f %f %f %f %lu\n",
                a.x, a.y, a.z, b.x, b.y, b.z, Y.points.size());

        X.removePoints(Y);
    } while ((X.points.size() > 1) &&
             ((opt_nlines == 0) || (opt_nlines > nlines)));

    delete hough;
    fclose(outfile);

    return 0;
}

//
// orthogonal least squares fit with libeigen
// rc = largest eigenvalue
//
