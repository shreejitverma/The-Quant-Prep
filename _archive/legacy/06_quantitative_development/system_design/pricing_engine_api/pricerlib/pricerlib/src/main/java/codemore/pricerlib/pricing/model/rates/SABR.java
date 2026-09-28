package codemore.pricerlib.pricing.model.rates;

import codemore.pricerlib.pricing.model.BlackScholes;
import codemore.pricerlib.pricing.option.pathindependent.rates.EuropeanCaplet;

import java.util.ArrayList;
import java.util.HashMap;

import static java.lang.Math.*;

public class SABR implements InterestRateModel { // Model parameters
    private double nu;
    private double alpha;
    private double beta;
    private double rho;
    private HashMap<String, Double> parameters;

    // Constructor
    public SABR(){
        // Declare default parameters for model
        nu = 0.5;
        alpha = 0.1;
        beta = 0.01;
        rho = -0.7;

        // Set all parameters into a hashmap
        this.parameters = new HashMap<>();
        this.parameters.put("nu", nu);
        this.parameters.put("alpha", alpha);
        this.parameters.put("beta", beta);
        this.parameters.put("rho", rho);
    }

    // Function to be used to calibrate model parameters
    public double calibrationErrorFunction(ArrayList<Double> parameters) {
        return 0.0;
    }

    // Get parameters as a hashmap
    public HashMap<String, Double> getParameters(){
        return parameters;
    };

    // Price a vanilla interest rate call option
    public double closedFormCapletPricer(EuropeanCaplet cap){
        /********************************************
         Simple SABR pricing formula for european cap options

         Model parmeters:
         alpha = initial volatility
         beta = conditionality parameter
         nu = volvol
         rho = correlation btwn vol & underlying

         Further information on: Managing Smile Risk (Hagan, Kumar, Lesniewski, Woodward)

         ********************************************/
        double forward = cap.getForward();
        double strike = cap.getStrike();
        double T = cap.getExpiry();
        double r = cap.getRate();

        // Calculate z
        double fkPowBeta = pow(forward * strike, (1 - beta)/2);
        double z = (nu/alpha) * fkPowBeta * Math.log(forward/strike);

        // Calculate x(z)
        double expXZNum = Math.sqrt(1 - 2 * rho * z + z*z) + z - rho;
        double expXZDenom = 1 - rho;
        double xz = Math.log(expXZNum/expXZDenom);

        // Calculate black volatility
        double elem1denom1 = (pow(1-beta, 2)/24) * pow(Math.log(forward/strike), 2);
        double elem1denom2 = (pow(1-beta, 4)/1920) * pow(Math.log(forward/strike), 4);
        double elem1denom = (1 + elem1denom1 + elem1denom2);
        double elem1 = alpha/(fkPowBeta * elem1denom) * (z /xz);

        // Second part
        double elem2part1 = (pow(1-beta, 2)/24) * (alpha * alpha)/pow(forward * strike, (1 - beta)/2);
        double elem2part2 = 0.25 * ((rho * beta * nu * alpha)/fkPowBeta);
        double elem2part3 = ((2 - 3*rho*rho)/24) * nu * nu;

        // Combine elements 1 and 2
        double volBlackScholes = elem1 * (1 + (elem2part1 + elem2part2 + elem2part3)*T);

        // Price using Black Scholes Model
        BlackScholes bsModel = new BlackScholes(volBlackScholes);
        double price = bsModel.closedFormCapletPricer(cap);

        return price;
    };
}
