package codemore.pricerlib.pricing.calibration;

import java.util.ArrayList;

public interface Calibrator {

    // Should provide parameters for any model
    ArrayList<Double> calibrate();
}
