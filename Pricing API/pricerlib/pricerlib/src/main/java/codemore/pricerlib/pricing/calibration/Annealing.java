package codemore.pricerlib.pricing.calibration;
import codemore.pricerlib.pricing.model.*;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

import static codemore.pricerlib.pricing.matlib.Matlib.*;

public class Annealing implements Calibrator {
    /***************************************************
     * Annealing class for calibration of models
     *
     * Parameters:
     *  DIM = number of model parameters
     *  CR = Crossover rate
     *  F = Mutation factor
     *  MAXITER = maximum iterations
     *
     * Returns:
     *  ArrayList of optimal parameters
     ****************************************************/
    int DIM;
    int NP;
    double CR;
    double F;
    int MAXITER;
    Model model;

    // Constructor
    Annealing(Model model){
        // Dimensions of the model
        this.DIM = model.getParameters().size();

        // Population
        this.NP = DIM * 10;
        
        // Cross over rate
        this.CR = 0.4;

        // Mutation Factor
        this.F = 0.5;

        // Maximum number of iterations
        this.MAXITER = 100000;
    }

    // Calibrate the model
    public ArrayList<Double> calibrate() {
        // Run while iterations are less than MAXITER
        int iterations = 0;

        // Container to hold all positions and evaluations
        ArrayList<ArrayList<Double>> allCandidates = new ArrayList<>(MAXITER);
        ArrayList<Double> allEvaluations = new ArrayList<>();

        while (iterations < MAXITER){
            // New Universe
            ArrayList<ArrayList<Double>> candidateUniverse;
            candidateUniverse = gaussianMatrix(NP, DIM);

            // Run algorithm on each candidateUniverse
            for (int i = 0; i < candidateUniverse.size(); i++) {
                // Select random indices in the candidateUniverse to use
                int index_a = ThreadLocalRandom.current().nextInt(0, NP);
                int index_b = ThreadLocalRandom.current().nextInt(0, NP);
                int index_c = ThreadLocalRandom.current().nextInt(0, NP);

                //Obtain Array elements
                ArrayList<Double> a = candidateUniverse.get(index_a);
                ArrayList<Double> b = candidateUniverse.get(index_b);
                ArrayList<Double> c = candidateUniverse.get(index_c);

                // Select random index
                int R = ThreadLocalRandom.current().nextInt(0, DIM);

                // Uniformly distributed number for each index
                ArrayList<Double> r = uniformArray(DIM);

                // Copy a value
                ArrayList<Double> y = candidateUniverse.get(i);

                // Apply crossover based on situations
                for (int j = 0; j < DIM; j++) {
                    if(r.get(j) <= CR || j == R){
                        y.set(j, a.get(j) +  F * (b.get(j) - c.get(j)));
                    } else{
                        ArrayList<Double> x = candidateUniverse.get(i);
                        y.set(j, x.get(j));
                    }
                }

                // To be used below
                ArrayList<Double> x = candidateUniverse.get(i);

                // Modify the candidate universe if missing objects
                if (model.calibrationErrorFunction(y) < model.calibrationErrorFunction(x)){
                    candidateUniverse.set(i, y);
                }

                // Add the number of iterations
                iterations += NP;

                // Append candidate to arraylist
                allCandidates.add(candidateUniverse.get(i));

                // Append function evaluation to arraylist
                allEvaluations.add(model.calibrationErrorFunction(candidateUniverse.get(i)));
            }
        }

        // Find the minimum of all evaluations
        double minEval = Collections.min(allEvaluations);
        int minIndex = allEvaluations.indexOf(minEval);

        // Return the corresponding parameter arrayList
        return allCandidates.get(minIndex);
    }
}
