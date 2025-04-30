import DDA.Network;
import static org.encog.persist.EncogDirectoryPersistence.*;

import java.io.File;

import engine.core.MarioGame;
import engine.core.MarioLevelGenerator;
import engine.core.MarioLevelModel;
import engine.core.MarioResult;
import engine.core.MarioTimer;

public class TrainDDA {
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
        MarioLevelGenerator generator = new levelGenerators.notch.LevelGenerator(1,2);
        double [] levelDiff = {generator.getDifficulty(),generator.getDifficulty(),generator.getDifficulty(),generator.getDifficulty()};
        //int tLoops = 1000;
        int lvl = 1;
        int successfullyTrained = 0;
        System.out.println( "Starting Difficulties: ");
        for(int j = 0; j<levelDiff.length;j++)
        {
            System.out.println(levelDiff[j]);
        }
        while(lvl<=50000)
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
                double[] correction = game.getDDA().critic(difficulties);
                
                //tell nn the correct adjustment parameters
                if (correction.length != 0)
                {
                    System.out.println("punishhh");
                    nn.train(performance, correction);
                    //nn.punish(correction);
                }
                //accept the nn's parameters if was correct
                else
                {
                    nn.train(performance, difficulties);
                    successfullyTrained += 1;
                    System.out.println("accepted diff");
                    //nn.accept();
                }
                //retrain nn with new player performance
            }
            else
            {
                // printResults(game.playGame(level, 200, 0));
                //generate a normal random level for first iteration
                String level = generator.getGeneratedLevel(new MarioLevelModel(500, 16), new MarioTimer(15 * 60 * 60 * 1000)); 
                printResults(game.runGame(new agents.trondEllingsen.Agent(), level, 60, 0, false));
                performance = game.getDDA().getTotalPerformance(true);
                //retrain nn with new player performance
                nn.train(performance,levelDiff);
            }
            //generate diffficulty for next level
            difficulties = nn.predictDifficulty(performance);
            lvl += 1;
            System.out.println( "New Difficulties: ");
            for(int j = 0; j<difficulties.length;j++)
            {
                System.out.println(difficulties[j]);
            }
        }
        
        System.out.println("Accepted: " + successfullyTrained);
        //loop number of times the levels is played
        //if greater than the first iteration
        saveObject(new File(filename),nn.getNN());
        //else run normal level generation
    }
}