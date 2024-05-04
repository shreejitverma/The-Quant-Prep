package codemore.pricerlib.pricing.matlib;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;
import static java.lang.Math.*;

public class Matlib {
    public static final double PI = 3.14159265358979323846;

    private static double randGauss(){
        /****************************************************
         * Implementation of the Gaussian CDF
         *
         * Using Box Muller implementation:
         * Z = Sqrt(-2 x ln U1) cos(2 x PI x U2)
         *
         ****************************************************/
        double U1 = ThreadLocalRandom.current().nextDouble();
        double U2 = ThreadLocalRandom.current().nextDouble();

        double result = sqrt( - 2.0 * Math.log(U1)) * Math.cos( 2 * Math.PI * U2);

        return result;
    }


    public static ArrayList<Double> gaussianArray(int length){
        /****************************************************
         * Matrix of Gaussian random variables
         *
         * Matrix form of randGauss
         ****************************************************/
        ArrayList<Double> result = new ArrayList<>(length);

        for (int i = 0; i < length; i++) {
            result.add(randGauss());
        }

        return result;
    }

    public static ArrayList<ArrayList<Double>> gaussianMatrix(int rows, int columns) {
        /****************************************************
         * ArrayList of ArrayLists of Gaussian random variables
         *
         * To be used in Annealing
         ****************************************************/
        // Array of Arrays
        ArrayList<ArrayList<Double>> result = new ArrayList<>();

        for (int i = 0; i < rows; i++) {
            // Create a new arrayList for each row
            ArrayList<Double> newRow = gaussianArray(columns);
            result.add(newRow);
        }

        return result;
    }
        public static ArrayList<Double> uniformArray(int length){
        /****************************************************
         * ArrayList of Uniform random variables
         *
         * ArrayList form of uniform
         ****************************************************/
        ArrayList<Double> result = new ArrayList<>(length);

        for (int i = 0; i < length; i++) {
            result.add(ThreadLocalRandom.current().nextDouble());
        }

        return result;
    }

    public static ArrayList<ArrayList<Double>> uniformMatrix(int rows, int columns){
        // Array of Arrays
        ArrayList<ArrayList<Double>> result = new ArrayList<>();

        for (int i = 0; i < rows; i++) {
            // Create a new arrayList for each row
            ArrayList<Double> newRow = uniformArray(columns);
            result.add(newRow);
        }

        return result;
    }

    public static double normPDF(double x){
        /****************************************************
        Calculate the probability distribution function of a standard gaussian
        ****************************************************/
        return exp(-0.5 * x*x)/sqrt(2 * PI);
    }

    public static double normPDF(double x, double mu, double sigma){
        /****************************************************
         Calculate the probability distribution function of a non standard gaussian

         Inputs:
         mu = Mean
         sigma = Std Deviation
         ****************************************************/
        return exp(-0.5 * pow((x-mu)/sigma, 2))/(sigma* sqrt(2 * PI));
    }

    private static double erf(double x){
        /****************************************************
        ERF approximation used to calculate Gaussian CDF

         More information about the implementation can be found here:
         Handbook of Mathematical Functions: with Formulas, Graphs, and Mathematical Tables
         Milton Abramowitz  Irene Stegun
         ****************************************************/
        //A&S formula 7.1.26
        double a1 = 0.254829592;
        double a2 = -0.284496736;
        double a3 = 1.421413741;
        double a4 = -1.453152027;
        double a5 = 1.061405429;
        double p = 0.3275911;
        x = Math.abs(x);
        double t = 1 / (1 + p * x);
        //Direct calculation using formula 7.1.26 is absolutely correct
        //But calculation of nth order polynomial takes O(n^2) operations
        //return 1 - (a1 * t + a2 * t * t + a3 * t * t * t + a4 * t * t * t * t + a5 * t * t * t * t * t) * Math.Exp(-1 * x * x);

        //Horner's method, takes O(n) operations for nth order polynomial
        return 1 - ((((((a5 * t + a4) * t) + a3) * t + a2) * t) + a1) * t * Math.exp(-1 * x * x);
    }


    public static double normCDF(double z){
        /****************************************************
         Calculate the cumulative distribution function of a standard gaussian using erf  approximation
         ****************************************************/
        double sign = 1;
        if (z < 0) sign = -1;

        double result=0.5 * (1.0 + sign * erf(Math.abs(z)/Math.sqrt(2)));
        return result;
    }

    public static double gamma(double z) {
        /****************************************
         Gamma Function
         Uses Lanczos approximation formula. See Numerical Recipes 6.1.

         *****************************************/
        double p0 = 1.000000000190015D;
        double p1 = 76.18009172947146D;
        double p2 = -86.50532032941678D;
        double p3 = 24.01409824083091D;
        double p4 = -1.231739572450155D;
        double p5 = 0.001208650973866179D;
        double p6 = -5.395239384953E-6D;
        double part1 = Math.sqrt(6.283185307179586D) / z;
        double part2 = p0 + p1 / (z + 1.0D) + p2 / (z + 2.0D) + p3 / (z + 3.0D) + p4 / (z + 4.0D) + p5 / (z + 5.0D) + p6 / (z + 6.0D);
        double part3 = Math.pow(z + 5.5D, z + 0.5D) * Math.exp(-(z + 5.5D));
        return part1 * part2 * part3;
    }
}
