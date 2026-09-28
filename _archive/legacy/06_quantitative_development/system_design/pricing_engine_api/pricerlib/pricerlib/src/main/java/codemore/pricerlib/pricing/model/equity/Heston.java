package codemore.pricerlib.pricing.model.equity;

import codemore.pricerlib.pricing.matlib.Complex;
import codemore.pricerlib.pricing.option.pathindependent.equity.EuropeanCall;

import java.util.ArrayList;
import java.util.HashMap;

import static java.lang.Math.*;

public class Heston implements EquityModel {
    // Model parameters
    private double sigma;
    private double kappa;
    private double theta;
    private double volvol;
    private double rho;
    private final Complex i;
    private HashMap<String, Double> parameters;

    // Constructor
    public Heston(double sigma, double kappa, double theta, double volvol, double rho){
        // Declare default parameters for model
        this.sigma = sigma;
        this.kappa = kappa;
        this.theta = theta;
        this.volvol = volvol;
        this.rho = rho;

        // Set all parameters into a hashmap
        this.parameters = new HashMap<>();
        this.parameters.put("sigma", sigma);
        this.parameters.put("kappa", kappa);
        this.parameters.put("theta", theta);
        this.parameters.put("volvol", volvol);
        this.parameters.put("rho", rho);
        this.i = new Complex(0, 1);

    }
    // Constructor
    public Heston(){
        // Declare default parameters for model
        sigma = 0.5;
        kappa = 0.1;
        theta = 0.01;
        volvol = 0.02;
        rho = -0.7;

        // Set all parameters into a hashmap
        this.parameters = new HashMap<>();
        this.parameters.put("sigma", sigma);
        this.parameters.put("kappa", kappa);
        this.parameters.put("theta", theta);
        this.parameters.put("volvol", volvol);
        this.parameters.put("rho", rho);
        this.i = new Complex(0, 1);
    }

    // Function to be used to calibrate model parameters
    public double calibrationErrorFunction(ArrayList<Double> parameters) {
        return 0.0;
    }

    // Get parameters as a hashmap
    public HashMap<String, Double> getParameters(){
        return parameters;
    }

    // Characteristic function of the heston pricer
    private Complex fHeston(Complex s, EuropeanCall call){
        double St = call.getSpot();
        double r = call.getRate();
        double T = call.getExpiry();

        // To be used subsequently
        double var = sigma*sigma;
        Complex onei = new Complex(1.0, 0.0);

        // Will be used a lot
        Complex prod = i.multiply(rho * sigma).multiply(s);

        // Calculate d
        Complex d1 = Complex.pow(prod.subtract(kappa), 2.0);

        Complex d21 = i.multiply(s).add(s.multiply(s));
        Complex d2 = d21.multiply(var);

        // Sqrt of sum of d1 and d2
        Complex d = Complex.pow(d1.add(d2), 0.5);

        // Calculate g
        Complex kappaComp = new Complex(kappa, 0);
        Complex g1 = kappaComp.subtract(prod.add(d));
        Complex g2 = kappaComp.subtract(prod.subtract(d));
        Complex g = g1.divide(g2);

        // Calculate first exponential. Split this into 3 parts

        //Part 1
        Complex expElem1 = i.multiply(s).multiply(log(St));
        Complex expElem2 = i.multiply(s).multiply(r * T);
        Complex exp1 = expElem1.multiply(expElem2);

        // Part2
        Complex dt = d.multiply(-T);
        Complex exp2 = g.multiply(Complex.exp(dt));

        // Part3
        Complex exp3 = onei.subtract(g);

        // Calculate first main exponential
        Complex mainExp1a = Complex.pow(exp2.divide(exp3), -2.0 * theta*kappa/var);
        Complex mainExp1 = exp1.multiply(mainExp1a);

        // Compute second exponential
        double exp4 = theta * kappa * T/ var;
        double exp5 = volvol/var;
        Complex exp6a = onei.subtract(Complex.exp(d.multiply(-T)));
        Complex exp6 = exp6a.divide(onei.subtract(g.multiply(Complex.exp(d.multiply(-T)))));

        // Compute second main exponential
        Complex mainExp2a = g1.multiply(exp4).add(g1.multiply(exp5).multiply(exp6));
        Complex mainExp2 = Complex.exp(mainExp2a);

        return mainExp1.add(mainExp2);
    }

    // Price a vanilla call option
    public double closedFormCallPricer(EuropeanCall call){
        Complex P = new Complex(0,0);
        double iterations = 1000.0;
        double maxNumber = 100.0;
        double ds = maxNumber/iterations;

        double St = call.getSpot();
        double K = call.getStrike();
        double r = call.getRate();
        double T = call.getExpiry();

        double element1 = 0.5 * (St - K * exp(- r * T));

        for (int j = 1; j <= iterations ; j++) {
            Complex s1 = new Complex(ds * (2*j+1)/2);
            Complex s2 = s1.subtract(i);

            Complex numerator1 = fHeston(s2, call);
            Complex numerator2 = fHeston(s1, call).multiply(K);
            Complex denominator1 = Complex.exp(i.multiply(log(K)).multiply(s1));
            Complex denominator = denominator1.multiply(i).multiply(s1);
            Complex subsetP = numerator1.subtract(numerator2).divide(denominator);
            P = P.add(subsetP.multiply(ds));
        }

        Complex element2 = P.divide(PI);
        double price = element2.add(element1).real();
        return price;
    }

    public double getSigma() {
        return sigma;
    }

    public void setSigma(double sigma) {
        this.sigma = sigma;
    }

    public double getKappa() {
        return kappa;
    }

    public void setKappa(double kappa) {
        this.kappa = kappa;
    }

    public double getTheta() {
        return theta;
    }

    public void setTheta(double theta) {
        this.theta = theta;
    }

    public double getVolvol() {
        return volvol;
    }

    public void setVolvol(double volvol) {
        this.volvol = volvol;
    }

    public double getRho() {
        return rho;
    }

    public void setRho(double rho) {
        this.rho = rho;
    }

    public void setParameters(HashMap<String, Double> parameters) {
        this.parameters = parameters;
    }
}
