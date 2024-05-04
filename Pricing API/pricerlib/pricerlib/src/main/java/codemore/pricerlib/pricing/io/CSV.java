package codemore.pricerlib.pricing.io;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class CSV {
    private Scanner sc;
    private String delimiter;
    private File file;
    private ArrayList<ArrayList<String>> fileList;

    public CSV(String fileLoc, String delimiter) throws FileNotFoundException {
        File file = new File(fileLoc);
        this.sc = new Scanner(file);
        this.delimiter = delimiter;
        fileList = new ArrayList<>();
    }

    // Use comma as default delimiter
    public CSV(String fileloc) throws FileNotFoundException{
        this(fileloc, ",");
    }

    public void print(){
        /************************
         * Read entire csv file and save it in list format
         * *************************/
        // Use colon as a delimiter
        sc.useDelimiter(",");

        // While another line exists print it out
        while(sc.hasNext()){
            System.out.print(sc.next() + "\t");
        }

        // Close scanner
        sc.close();
    }

    public ArrayList<ArrayList<String>> read(){
        /************************
         * Print out entire csv file
         * *************************/
        // Use colon as a delimiter
        sc.useDelimiter(delimiter);

        // While another line exists print it out
        while(sc.hasNext()){
            String[] line = sc.nextLine().split(delimiter);
            ArrayList<String> row = new ArrayList<>(Arrays.asList(line));
            fileList.add(row);
        }
        // Close scanner
        sc.close();

        return fileList;
    }
}
