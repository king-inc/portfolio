package DDA;
import java.io.*;
import java.net.*;

public class JavaClient {
    public static double[] getDifficulty(double[] input) {
        double[] diff = new double[4];
        String diffStr = "";
        String inputStr = convInput(input);

        String hostName = "Inc";
        int portNumber = 8000;
        try (
            Socket clientSocket = new Socket(hostName, portNumber);
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in))
            ) {
                out.println(inputStr);
                diffStr = in.readLine();
                
                //while ((userInput = stdIn.readLine()) != null) {
                    //out.println(userInput);
                    //System.out.println("Server: " + in.readLine());
                    //}
                } catch (UnknownHostException e) {
                    System.err.println("Don't know about host " + hostName);
                    System.exit(1);
                } catch (IOException e) {
                    System.err.println("Couldn't get I/O for the connection to " +
                    hostName);
                    System.exit(1);
                }
                
            diff = convOut(diffStr);
            return diff;
    }

    static String convInput(double[] input)
    {
        String out = "";
        for (int i=0; i<input.length; i++)
        {
            if (i < input.length-1)
            {
                out += input[i] + ",";
            }
            else
            {
                out += input[i];
            }
        }

        return out;
    } 

    static double[] convOut(String outStr)
    {
        System.out.println(outStr);
        outStr = outStr.replace("\n", "");
        outStr = outStr.replace("\r", "");
        double[] out = new double[4];
        String[] outList = outStr.split(",");
        for (int i =0; i<out.length; i++)
        {
            //System.out.println(outList[i]);
            out[i] = Double.parseDouble(outList[i]);
        }
        return out;
    }
}
