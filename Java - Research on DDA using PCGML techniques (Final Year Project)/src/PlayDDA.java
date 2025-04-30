import java.io.IOException;

import DDA.JavaClient;
import engine.core.MarioGame;
import engine.core.MarioLevelGenerator;
import engine.core.MarioLevelModel;
import engine.core.MarioResult;
import engine.core.MarioTimer;
import java.util.ArrayList;
import java.util.List;

public class PlayDDA {
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
        MarioLevelGenerator generator = new levelGenerators.notch.LevelGenerator(2,2);
        double [] levelDiff = {generator.getDifficulty(),generator.getDifficulty(),generator.getDifficulty(),generator.getDifficulty()};
        double[] performance;
        MarioGame game = new MarioGame();
        int tries = 6;
        while(tries>0)
        {
            game.getDDA().saveDiff(levelDiff);
            String level = generator.getGeneratedLevel(new MarioLevelModel(500, 16), new MarioTimer(5 * 60 * 60 * 1000),levelDiff);
            printResults(game.runGame(new agents.human.Agent(), level, 120, 0, true));
            performance = game.getDDA().getTotalPerformance(false);
            game.getDDA().level += 1;
            if(tries-1>0)
            {
                levelDiff = JavaClient.getDifficulty(performance);
            }
            tries -= 1;

        }
        // printResults(game.playGame(level, 200, 0));
    }
}
