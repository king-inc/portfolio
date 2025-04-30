import DDA.NN;
import DDA.Network;
import static org.encog.persist.EncogDirectoryPersistence.*;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.encog.ml.data.MLDataPair;
import org.encog.ml.data.MLDataSet;
import org.encog.ml.data.basic.BasicMLData;
import org.encog.ml.data.basic.BasicMLDataPair;
import org.encog.ml.data.basic.BasicMLDataSet;

import engine.core.MarioGame;
import engine.core.MarioLevelGenerator;
import engine.core.MarioLevelModel;
import engine.core.MarioResult;
import engine.core.MarioTimer;

public class TrainDDA2 {
    public static void printResults(MarioResult result) {
        System.out.println("****************************************************************");
        System.out.println("Game Status: " + result.getGameStatus().toString() +
                " Percentage Completion: " + result.getCompletionPercentage());
        System.out.println("Lives: " + result.getCurrentLives() + " Coins: " + result.getCurrentCoins() +
                " Remaining Time: " + (int) Math.ceil(result.getRemainingTime() / 1000f));
        System.out.println("Mario State: " + result.getMarioMode() +
                " (Mushrooms: " + result.getNumCollectedMushrooms() + " Fire Flowers: " + result.getNumCollectedFireflower() + ")");
        System.out.println("Total Kills: " + result.getKillsTotal() + " (Stomps: " + result.getKillsByStomp() +
                " Fireballs: " + result.getKillsByFire() + " Shells: " + result.getKillsByShell() +
                " Falls: " + result.getKillsByFall() + ")");
        System.out.println("Bricks: " + result.getNumDestroyedBricks() + " Jumps: " + result.getNumJumps() +
                " Max X Jump: " + result.getMaxXJump() + " Max Air Time: " + result.getMaxJumpAirTime());
        System.out.println("****************************************************************");
    }

    public static void main(String[] args) {
        MarioGame game = new MarioGame();
        String filename = "C:\\Users\\incre\\Downloads\\Mario-AI-Framework-master\\src\\model\\network4.eg";
        //init Network
        Network nn = new Network();
        double[] performance;
        double[] difficulties = {};
        MLDataSet trainingData = new BasicMLDataSet();
        MarioLevelGenerator generator = new levelGenerators.notch.LevelGenerator(1,2);
        double[][] dPerformance = new double[1000][4];
        double[][] dDifficulty = new double[1000][4];
        double [] levelDiff = {generator.getDifficulty(),generator.getDifficulty(),generator.getDifficulty(),generator.getDifficulty()};
        //int tLoops = 1000;
        int lvl = 1;
        int successfullyTrained = 0;
        List<double[]> out = new ArrayList<double[]>();
        System.out.println( "Starting Difficulties: ");
        for(int j = 0; j<levelDiff.length;j++)
        {
            System.out.println(levelDiff[j]);
        }
        while(lvl<=1000)
        {
            System.out.println(("GAME " + lvl ));
            //after first iteration
            if(lvl>1)
            {
                // printResults(game.playGame(level, 200, 0));
                //generate level with adjusted difficulties from nn
                String level = generator.getGeneratedLevel(new MarioLevelModel(500, 16), new MarioTimer(15 * 60 * 60 * 1000), difficulties);
                printResults(game.runGame(new agents.trondEllingsen.Agent(), level, 60, 0, false));
                //get player performance from DDA
                performance = game.getDDA().getTotalPerformance(true);
                // critic nn's generated difficulties for the level with player's performance
                //double[] correction = game.getDDA().critic(difficulties,false);
            }
            else
            {
                // printResults(game.playGame(level, 200, 0));
                //generate a normal random level for first iteration
                String level = generator.getGeneratedLevel(new MarioLevelModel(500, 16), new MarioTimer(15 * 60 * 60 * 1000)); 
                printResults(game.runGame(new agents.trondEllingsen.Agent(), level, 60, 0, false));
                performance = game.getDDA().getTotalPerformance(true);
                //retrain nn with new player performance
                //nn.train(performance,levelDiff);
            }
            //generate diffficulty for next level
            difficulties = game.getDDA().critic();
            dPerformance[lvl-1] = performance;
            dDifficulty[lvl-1] = difficulties; 
            double [] entry = {0,0,0,0,0,0,0,0};
            for(int i = 0; i<8; i++)
            {
                if (i<4)
                {
                    entry[i] = performance[i];
                }
                else
                {
                    entry[i] = difficulties[i-4];
                } 
            }

            out.add(entry);
                
            MLDataPair correct = new BasicMLDataPair(
            new BasicMLData(performance),
            new BasicMLData(difficulties));

            trainingData.add(correct);

            lvl += 1;
            System.out.println( "New Difficulties: ");
            for(int j = 0; j<difficulties.length;j++)
            {
                System.out.println(difficulties[j]);
            }
        }
        FileWriter writer;
        try {
            writer = new FileWriter("./dataset.csv");
            for (int i = 0; i<1000; i++)
            {
                for(int j = 0; j<8; j++)
                {
                    writer.append(String.valueOf(out.get(i)[j]));
                    if(j<7)
                    {
                        writer.append(",");
                    }
                }
                writer.append("\n");
            }
            writer.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        System.out.println("Accepted: " + successfullyTrained);

        NN.train(dPerformance,dDifficulty);
        //nn.train(trainingData);
        //loop number of times the levels is played
        //if greater than the first iteration
        //saveObject(new File(filename),nn.getNN());
        //else run normal level generation
    }
}