package codemore.pricerlib.pricing.option.pathindependent.rates;

import codemore.pricerlib.pricing.model.Model;
import codemore.pricerlib.pricing.option.pathindependent.PathIndependentOption;

import java.util.ArrayList;

public class EuropeanPayerSwaption implements PathIndependentOption {
    private ArrayList<Double> zcCurve;
    private double strike, forwardSwapRate;
    private double expiry, tenor;

    EuropeanPayerSwaption(){
    }

    EuropeanPayerSwaption(ArrayList<Double> zcCurve, double strike, double expiry, double tenor){
        this.zcCurve = zcCurve;
        this.strike = strike;
        this.expiry = expiry;
        this.tenor = tenor;
        this.forwardSwapRate = forwardSwapRate();
    }

    private double forwardSwapRate(){
        /******************************
         * Calculate the forward swap rate from the zero coupon curve
         *****************************/
        return 0;
    }

    public double price(Model model) {
        return 0;
    }

    public ArrayList<Double> getZcCurve() {
        return zcCurve;
    }

    public void setZcCurve(ArrayList<Double> zcCurve) {
        this.zcCurve = zcCurve;
    }

    public double getStrike() {
        return strike;
    }

    public void setStrike(double strike) {
        this.strike = strike;
    }

    public double getForwardSwapRate() {
        return forwardSwapRate;
    }

    public void setForwardSwapRate(double forwardSwapRate) {
        this.forwardSwapRate = forwardSwapRate;
    }

    public double getExpiry() {
        return expiry;
    }

    public void setExpiry(double expiry) {
        this.expiry = expiry;
    }

    public double getTenor() {
        return tenor;
    }

    public void setTenor(double tenor) {
        this.tenor = tenor;
    }

}
