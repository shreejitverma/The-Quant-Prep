package codemore.pricerlib.pricing.option.pathindependent.rates;

import codemore.pricerlib.pricing.model.Model;
import codemore.pricerlib.pricing.model.rates.InterestRateModel;
import codemore.pricerlib.pricing.option.pathindependent.PathIndependentOption;

public class EuropeanCaplet implements PathIndependentOption<InterestRateModel> {
    private double strike, forward, spot;
    private double expiry, rate;

    public EuropeanCaplet(){
        spot = 110;
        forward = 105;
        strike = 100;
        expiry = 1;
        rate = 0.01;
    }

    public double price(InterestRateModel model){
        return model.closedFormCapletPricer(this);
    }

    //public double price(Model model) {return 0;}
    public double getStrike() {
        return strike;
    }

    public void setStrike(double strike) {
        this.strike = strike;
    }

    public double getForward() {
        return forward;
    }

    public void setForward(double forward) {
        this.forward = forward;
    }

    public double getSpot() {
        return spot;
    }

    public void setSpot(double spot) {
        this.spot = spot;
    }

    public double getExpiry() {
        return expiry;
    }

    public void setExpiry(double expiry) {
        this.expiry = expiry;
    }

    public double getRate() {
        return rate;
    }

    public void setRate(double rate) {
        this.rate = rate;
    }


}
