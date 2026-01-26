package codemore.pricerlib.pricing.option.pathindependent.equity;
import codemore.pricerlib.pricing.model.*;
import codemore.pricerlib.pricing.model.equity.EquityModel;
import codemore.pricerlib.pricing.option.pathindependent.PathIndependentOption;

public class EuropeanCall implements PathIndependentOption<EquityModel> {
    private double strike, forward, spot;
    private double expiry, rate;

    public EuropeanCall(){
        spot = 110;
        forward = 105;
        strike = 100;
        expiry = 1;
        rate = 0.01;
    }

    public double price(EquityModel model){
        return model.closedFormCallPricer(this);
    }

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
