package codemore.pricerlib.pricing.model.equity;

import codemore.pricerlib.pricing.matlib.Complex;
import codemore.pricerlib.pricing.matlib.Matlib;
import codemore.pricerlib.pricing.option.pathindependent.equity.EuropeanCall;

import java.util.ArrayList;
import java.util.HashMap;

import static java.lang.Math.pow;

public class RoughHeston implements EquityModel{
    // Model parameters
    private double lambda;
    private double gamma;
    private double theta;
    private double v0;
    private double rho;
    private double alpha;

    private final Complex i = new Complex(0, 1);
    private final int N = 1000;
    private final int iterations = 1000;
    private final int maxNumber = 100;
    private double[][] a,b;

    private HashMap<String, Double> parameters;

    public RoughHeston(double lambda, double gamma, double theta, double v0, double rho, double alpha) {
        this.lambda = lambda;
        this.gamma = gamma;
        this.theta = theta;
        this.v0 = v0;
        this.rho = rho;
        this.alpha = alpha;

        // Set all parameters into a hashmap
        this.parameters = new HashMap<>();
        this.parameters.put("lambda", lambda);
        this.parameters.put("gamma", gamma);
        this.parameters.put("theta", theta);
        this.parameters.put("v0", v0);
        this.parameters.put("rho", rho);
        this.parameters.put("alpha", alpha);

    }

    public RoughHeston() {
        this.lambda = 0.1;
        this.gamma = 0.331;
        this.theta = 0.3156;
        this.v0 = 0.0392;
        this.rho = -0.681;
        this.alpha = 0.62;

        // Set all parameters into a hashmap
        this.parameters = new HashMap<>();
        this.parameters.put("lambda", lambda);
        this.parameters.put("gamma", gamma);
        this.parameters.put("theta", theta);
        this.parameters.put("v0", v0);
        this.parameters.put("rho", rho);
        this.parameters.put("alpha", alpha);
    }

    @Override
    public HashMap<String, Double> getParameters() {
        return parameters;
    }

    private Complex fRiccati(Complex x, Complex u){
        /***************************
         * Implementation of the fractional Riccati for the characteristic function of the rough Heston
         *
         * F(a,x) = 0.5 * (-u^2 - i*u) + λ(i*u*ρ*ν−1) * 0.5 * (λ*ν*x)^2
         * **************************/
        Complex usquared = u.multiply(u);
        Complex iu = i.multiply(u);
        Complex section1 = usquared.add(iu).multiply(-0.5);

        Complex iuRho = iu.multiply(rho*gamma).subtract(1);
        Complex section2 = iuRho.multiply(x).multiply(lambda);

        Complex section3 = Complex.pow(x.multiply(gamma*lambda), 2);
        section3 = section3.divide(2);

        Complex result = section1.add(section2).add(section3);
        return result;

    }

    private Complex phi(Complex u, double T){
        Complex[] h_a_tk;
        Complex[] F_a_h_tk;
        Complex[] h_p;

        h_a_tk = new Complex[N+1];
        F_a_h_tk = new Complex[N+1];
        h_p = new Complex[N+1];

        Complex complex0 = new Complex(0,0);
        F_a_h_tk[0] = fRiccati(complex0, u);

        for (int j = 0; j < N; j++) {


        }

        return i;
    }

    private void loadAdamsWeights(double dt){
        this.a = new double[N][N];
        this.b = new double[N][N];


        for (int k = 0; k < N; k++) {
            // Calculate weights for a
            this.a[k][0] = pow(dt, alpha) * (pow(k, alpha+1) - ((k - alpha) * pow(k+1, alpha)))/ Matlib.gamma(alpha + 2);

            for (int j = 0; j < k; j++) {
                this.a[k][j+1] = pow(dt, alpha) * (pow(k- j + 2, alpha+1) +
                                                pow(k - j, alpha + 1) -
                                                2 * pow(k - j + 1, alpha + 1))/Matlib.gamma(alpha + 2);
            }

            // Calculate weights for b
            for (int j = 0; j < k; j++) {
                this.b[k][j] = pow(dt, alpha) * (pow(k- j + 1, alpha) - pow(k- j,alpha))/Matlib.gamma(alpha + 1);
            }

        }

    }

    @Override
    public double closedFormCallPricer(EuropeanCall europeanOption) {
        double St = europeanOption.getSpot();
        double K = europeanOption.getStrike();
        double r = europeanOption.getRate();
        double T = europeanOption.getExpiry();

        double dt = T/N;

        // Load Adams weights
        loadAdamsWeights(dt);

        // Mid point rule integral calculation


        return 0;
    }

    @Override
    public double calibrationErrorFunction(ArrayList<Double> parameters) {
        return 0;
    }

    public double getLambda() {
        return lambda;
    }

    public void setLambda(double lambda) {
        this.lambda = lambda;
    }

    public double getGamma() {
        return gamma;
    }

    public void setGamma(double gamma) {
        this.gamma = gamma;
    }

    public double getTheta() {
        return theta;
    }

    public void setTheta(double theta) {
        this.theta = theta;
    }

    public double getV0() {
        return v0;
    }

    public void setV0(double v0) {
        this.v0 = v0;
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
