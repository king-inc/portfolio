package DDA;
import org.encog.app.analyst.EncogAnalyst;
import org.encog.app.analyst.wizard.AnalystWizard;
import org.encog.engine.network.activation.ActivationSigmoid;
import org.encog.engine.network.activation.ActivationTANH;
import org.encog.ml.data.MLData;
import org.encog.ml.data.MLDataPair;
import org.encog.ml.data.MLDataSet;
import org.encog.ml.data.basic.BasicMLData;
import org.encog.ml.data.basic.BasicMLDataPair;
import org.encog.ml.data.basic.BasicMLDataSet;
import org.encog.neural.networks.training.Train;
import org.encog.neural.networks.BasicNetwork;
import org.encog.neural.networks.layers.BasicLayer;
import org.encog.neural.networks.training.propagation.back.Backpropagation;
import org.encog.neural.networks.training.propagation.resilient.ResilientPropagation;


public class Network {
    private int inputSize = 4;
    private int hiddenSize = 10;
    private int outputSize = 4;
    private MLDataSet trainingData;
    private MLDataSet prevTrainingData;
    private double[] prevPerformance = {};
    private BasicNetwork network;

    public Network()
    {
        this.network = new BasicNetwork();
        network.addLayer(new BasicLayer(null, true, inputSize));
        network.addLayer(new BasicLayer(new ActivationTANH(), true, hiddenSize));
        network.addLayer(new BasicLayer(new ActivationTANH(), true, hiddenSize*2));
        network.addLayer(new BasicLayer(new ActivationTANH(), true, hiddenSize));
        network.addLayer(new BasicLayer(new ActivationTANH(), true, outputSize));
        network.getStructure().finalizeStructure();
        network.reset();
    }
    public BasicNetwork  getNN()
    {
        return this.network;
    }
    public void train(MLDataSet trainingDataset)
    {
        final Train train = new ResilientPropagation(network, trainingDataset);
        int epoch = 1;

        do {
            train.iteration();
            if(epoch <20 )
            {
                System.out.println("Epoch #" + epoch + " Error:" + train.getError());

            }
            epoch++;
        } while(train.getError()>0.1);

        //train.finishTraining();
    }

    public void train(double[] performance, double[] difficulties)
    {

        prevPerformance = performance;
        double[][] dPerformance = {{0}};
        double[][] dDifficulties = {{0}};
        dPerformance[0] = performance;
        dDifficulties[0] = difficulties;
        //prevTrainingData.add(dPerformance, dDifficulties);
        trainingData = new BasicMLDataSet(dPerformance, dDifficulties);

        final Train train = new Backpropagation(network, trainingData);
        int epoch = 1;

        do {
            train.iteration();
            if(epoch==1 || epoch==499999)
            {
                System.out.println("Epoch #" + epoch + " Error:" + train.getError());
            } 
            epoch++;
        } while(epoch < 500000);
        
        //train.finishTraining();
    }

    public double[] predictDifficulty(double[] playerPerformance)
    {
        MLData input = new BasicMLData(playerPerformance);

        double[] output = network.compute(input).getData();
        return output;
    }

}
