package DDA;

import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.ArrayList;
import engine.core.MarioResult;
import engine.core.MarioAgentEvent;
import engine.helper.GameStatus;

public class DDA {
    public int newDifficulty = 1;
    //private int avgTimeSpent;
    //teh average variables are the average of the parameter over ten seconds
    private int avgKills = 1;
    private int avgCoinsCollected = 25;
    private int avgActionsPerfomed = 300;
    private int avgDistance = 130;
    private int avgJumps = 10;
    private int timeSpent;
    private int prevTime = 0;
    private int distanceTravelled = 0;
    private int totalKills = 0;
    private int totalCoins = 0;
    private int totalActionsPerformed = 0;
    private int totalJumpsPerformed = 0;
    private int[] parameterDiff = {1,1,1,1};
    private boolean wonLevel = false;
    private double winPercentage = 0;
    public int level = 1;

    public int userId = 11;


    //private int died, wins = 0;
    //private List<Integer> ist = new ArrayList<>();
    private HashMap<Integer, Integer[]> stats = new HashMap<Integer, Integer[]>();


    public void monitor(int timeSpentOnLevel, int lengthOfLevelPassed, MarioResult result ) throws IOException {
        timeSpent = timeSpentOnLevel;
        //System.out.println(timeSpent);
        //System.out.print("Here!!!!!!!!!!!!!!!!!!!!!!!!");
        //record stats every ten seconds
        if (result.getGameStatus() == GameStatus.WIN || result.getGameStatus() == GameStatus.LOSE)
        {
            recordStats(lengthOfLevelPassed, result.getKillsTotal(), result.getCurrentCoins(),countActions(result.getAgentEvents()), result.getNumJumps());
            wonLevel = result.getGameStatus() == GameStatus.WIN; 
            winPercentage = result.getCompletionPercentage();
            //saveStats();
            // make a list of total stats and death and pass to NN
            //update total stats
            distanceTravelled = 0;
            totalKills = 0;
            totalCoins = 0;
            totalActionsPerformed = 0;
            totalJumpsPerformed = 0;
            prevTime = 0;
            System.out.println(String.format("Won: %s", wonLevel));
            System.out.println("----------------------------------------------------");
            
        }
        else if (timeSpent % 10 == 0 && timeSpent != prevTime)
        {
            recordStats(lengthOfLevelPassed, result.getKillsTotal(), result.getCurrentCoins(),countActions(result.getAgentEvents()), result.getNumJumps());
            
            //update total stats
            distanceTravelled = lengthOfLevelPassed;
            totalKills = result.getKillsTotal();
            totalCoins = result.getCurrentCoins();
            totalActionsPerformed = countActions(result.getAgentEvents());
            totalJumpsPerformed = result.getNumJumps();
            prevTime = timeSpent;
            
        }
        
    }

    public int generateDifficulty(int difficulty)
    {
        // score their performance based on stats and average stats
        int scoreDistance = 10;
        int scoreKills = 10;
        int scoreCoins = 10;
        int scoreActions = 10;
        int scoreJumps = 10;
        int overallScore;

        for (HashMap.Entry<Integer,Integer[]> stat : stats.entrySet() )
        {
            scoreDistance += stat.getValue()[0] - avgDistance;
            scoreKills += stat.getValue()[1] - avgKills;
            scoreCoins += stat.getValue()[2] - avgCoinsCollected;
            //TO DO - compute action over distance covered every ten seconds to determine actions perfromed
            scoreActions += stat.getValue()[3] - avgActionsPerfomed;
            //jumps dont contribute to overall level difficulty
            scoreJumps += stat.getValue()[4] - avgJumps; 
        }
        //change magnitude of certain stats to 30 and score performance over 100
        scoreDistance = (scoreDistance * 30 )/ 20;
        scoreActions = (scoreActions * 30) / 20;

        overallScore = scoreActions + scoreCoins + scoreDistance + scoreKills;
        
        if(overallScore >= 55 && overallScore <70)
        {
            newDifficulty = difficulty + 1;
        }
        else if(overallScore >= 70 && overallScore <80)
        {
            newDifficulty = difficulty + 2;
        }
        else if(overallScore >= 80 )
        {
            newDifficulty = difficulty + 3;
        }
        else if(overallScore >= 40 && overallScore <55)
        {
            newDifficulty = difficulty - 1;
        }
        else if(overallScore >= 30 && overallScore <40)
        {
            newDifficulty = difficulty - 2;
        }
        else if(overallScore <20)
        {
            newDifficulty = difficulty - 3;
        }
        //add base case for negative diffiulty
        //add win or death
        //or check if its acc necessary
        //fix overall to float
        //individual parameter difficulties

        return newDifficulty;
    }

    public int[] generateParameterDiff(int difficulty)
    {
        System.out.println("so this runs okay");
        if (stats.isEmpty())
        {
            return parameterDiff;
        }
        else
        {

            // score their performance based on stats and average stats
            int scoreDistance = 10;
            int scoreKills = 10;
            int scoreCoins = 10;
            int scoreActions = 10;
            int overallScore;
    
            for (HashMap.Entry<Integer,Integer[]> stat : stats.entrySet() )
            {
                scoreDistance += stat.getValue()[0] - avgDistance;
                scoreKills += stat.getValue()[1] - avgKills;
                scoreCoins += stat.getValue()[2] - avgCoinsCollected;
                //TO DO - compute action over distance covered every ten seconds to determine actions perfromed
                scoreActions += stat.getValue()[3] - avgActionsPerfomed;
    
            }
            //change magnitude of certain stats to 30 and score performance over 100
            scoreDistance = (scoreDistance * 30 )/ 20;
            scoreActions = (scoreActions * 30) / 20;
    
            overallScore = scoreActions + scoreCoins + scoreDistance + scoreKills;
            
            if(overallScore >= 55 && overallScore <70)
            {
                newDifficulty = difficulty + 1;
            }
            else if(overallScore >= 70 && overallScore <80)
            {
                newDifficulty = difficulty + 2;
            }
            else if(overallScore >= 80 )
            {
                newDifficulty = difficulty + 3;
            }
            else if(overallScore >= 40 && overallScore <55)
            {
                newDifficulty = difficulty - 1;
            }
            else if(overallScore >= 30 && overallScore <40)
            {
                newDifficulty = difficulty - 2;
            }
            else if(overallScore <20)
            {
                newDifficulty = difficulty - 3;
            }
            //add base case for negative diffiulty
            //add win or death
            //or check if its acc necessary
            parameterDiff[0] =  newDifficulty;
    
            
            //2nd parameter for adjusting the odds of cannons spawning
            //3rd parameter for increasing or decreasing number and difficulty of enemy
            if (scoreKills >= 12  && scoreKills<15)
            {
                parameterDiff[3] += 2;
            }
            else if (scoreKills >= 8  && scoreKills<12)
            {
                parameterDiff[3] += 1;
            }
            else if (scoreKills<8)
            {
                parameterDiff[3] -= 1;
            }
            else if (scoreKills >= 15 )
            {
                parameterDiff[3] += 2;
                parameterDiff[2] += 1;
            }
    
            //reduce 1 from parameters if players die
            if(wonLevel != false )
            {
                parameterDiff[3] -= 1;
            }
    
            System.out.println("Stats: ");
            for (int i = 0; i<parameterDiff.length; i++ )
            {
                System.out.println(parameterDiff[i]);
            }
    
            saveStats();
            return parameterDiff;
        }
    }
    
    public void saveDiff(double[] diff)
    {
        //int userId = 0;
        FileWriter writer;
        try {
            writer = new FileWriter(("./performance_data/diff_user_"+ String.valueOf(userId)+ ".csv"), true);
            writer.append(String.valueOf(level)+",");
            //writer.append("Time_Spent,Distance_Covered,Kills,Coins,Actions_Performed,Jumps_Performed\n");
            for(int i = 0; i<diff.length; i++ )
            {
                writer.append(String.valueOf(diff[i]));
                if(i<diff.length-1)
                {
                    writer.append(",");
                }
            }
            writer.append("\n");
            writer.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    public void saveStats()
    {
        //int userId = 0;
        FileWriter writer;
        try {
            writer = new FileWriter(("./performance_data/user_"+ String.valueOf(userId)+ ".csv"), true);
            //writer.append("Time_Spent,Distance_Covered,Kills,Coins,Actions_Performed,Jumps_Performed\n");
            for(HashMap.Entry<Integer,Integer[]> stat : stats.entrySet() )
            {
                writer.append(String.valueOf(level)+",");
                writer.append(String.valueOf(stat.getKey()));
                writer.append(",");
                for(int i = 0; i<5; i++)
                {
                    writer.append(String.valueOf(stat.getValue()[i]));
                    if(i<4)
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
        //save stats into file
        wonLevel = false; 
        //each player can have multiple runs in their file
    }

    private void recordStats(int lengthOfLevelPassed, int killsTotal, int numberOfGainedCoins, int totActionsPerformed, int jumpActionsPerformed)
    {
    //record stat change in those 10 seconds
    int currentdistanceTravelled = lengthOfLevelPassed - distanceTravelled;
    int currentKills = killsTotal - totalKills;
    int currentCoins = numberOfGainedCoins - totalCoins;
    int currentActionsPerformed = totActionsPerformed - totalActionsPerformed;
    int currentJumpsPerformed = jumpActionsPerformed - totalJumpsPerformed;
    //put in stat dictionary
    try{
        stats.put(timeSpent, new Integer[]{currentdistanceTravelled,currentKills,currentCoins,currentActionsPerformed, currentJumpsPerformed});
    }
    catch (Exception e)
    {
        System.out.println("problem here");
    }
    System.out.println(String.format("Current Time Spent: %s", timeSpent));
    System.out.println(String.format("Prev Time Spent: %s", prevTime));
    System.out.println(String.format("Current Distance Travelled: %s", currentdistanceTravelled));
    System.out.println(String.format("Current Kills: %s", currentKills));
    System.out.println(String.format("Current Coins: %s", currentCoins));
    System.out.println(String.format("Current Actions Performed: %s", currentActionsPerformed));
    System.out.println(String.format("Current Jumps Performed: %s", currentJumpsPerformed));
    System.out.println("----------------------------------------------------");
    }

    private int countActions(ArrayList<MarioAgentEvent> actions)
    {
        int i_Actions = 0;
        for(MarioAgentEvent e : actions)
        {
            i_Actions += 1;   
        }
        return i_Actions;
    }
    
    public double[] getTotalPerformance(boolean training)
    {
        double[] performance = {0,0,0,0};
        int jump = 0;
        //int actions = 0; 
        for (HashMap.Entry<Integer,Integer[]> stat : stats.entrySet() )
        {
            performance[1] += stat.getValue()[1];
            //performance[2] += stat.getValue()[2];
            //actions += stat.getValue()[3];
            jump += stat.getValue()[4];
        }
        //performance[0] += stat.getKey();
        performance[0] = timeSpent;
        performance[0] = Util.norm(performance[0]);
        performance[2] = jump;
        performance[3] = winPercentage;

        //System.out.println(String.format("Total Time Spent: %s", performance[0]));
        System.out.println(String.format("Total Distance Travelled: %s", performance[0]));
        System.out.println(String.format("Total Kills: %s", performance[1]));
        System.out.println(String.format("Total Jumps: %s", performance[2]));
        System.out.println(String.format("Completion Percentage: %s", performance[3]));
        System.out.println("----------------------------------------------------");
        
        if(!training)
        {
            saveStats();
            stats.clear();
        }
        
        return performance;
    }

    public double[] critic()
{
    //double[] noCorrection = {};
    double[] correction ={1,1,1,1};
    // score their performance based on stats and average stats
    int scoreDistance = 10;
    int scoreKills = 10;
    //int scoreCoins = 10;
    int jumps = 10;
    //int actions = 0;
    //int jumpFreq;

    for (HashMap.Entry<Integer,Integer[]> stat : stats.entrySet() )
    {

        //implement avg distance of ten seconds critc path (reduce enemy line and cannon, reduce tubes)
        //win percentage closer to winning means increase more difficult if lower reduce
        if(stat.getKey() <10)
        {
            scoreDistance += stat.getValue()[0] - ((avgDistance*stat.getKey())/10);
            scoreKills += stat.getValue()[1] - ((avgKills*stat.getKey())/10);
            //actions += stat.getValue()[3];
            jumps += stat.getValue()[4] - ((avgJumps*stat.getKey())/10);
        }
        else
        {

            scoreDistance += stat.getValue()[0] - avgDistance;
            scoreKills += stat.getValue()[1] - avgKills;
            //actions += stat.getValue()[3];
            jumps += stat.getValue()[4] - avgJumps;
            //TO DO - compute action over distance covered every ten seconds to determine actions perfromed
        }

    }
    //jumpFreq = jumps/actions;

    //change magnitude of certain stats to 30 and score performance over 100
    //scoreDistance = (scoreDistance * 30 )/ 20;
    //scoreActions = (scoreActions * 30) / 20;

    //add base case for negative diffiulty
    //add win or death
    //or check if its acc necessar

    
    //2nd parameter for adjusting the odds of cannons spawning
    //3rd parameter for increasing or decreasing number and difficulty of enemy
    if(scoreDistance >= 15)
    {
        correction[0] += 2;
        correction[1] += 1;
        correction[2] += 2;
        correction[3] += 2;
    }
    else if(scoreDistance >= 12 && scoreDistance < 15)
    {
        correction[0] += 1;
        correction[1] += 1;
        correction[2] += 1;
    }
    else if(scoreDistance >= 8 && scoreDistance < 12)
    {
        correction[0] += 1;
    }
    else
    {
        correction[0] -= 1;
        correction[1] -= 1;
        correction[2] -= 1;
    }

    if (scoreKills >= 12  && scoreKills<15)
    {
        correction[0] += 2;
        correction[3] += 2;
    }
    else if (scoreKills >= 8  && scoreKills<12)
    {
        correction[0] += 2;
    }
    else if(scoreKills<8 && wonLevel)
    {
        correction[0] += 2;
    }
    else if (scoreKills<8)
    {
        correction[0] -= 1;
    }
    else if (scoreKills >= 15 )
    {
        correction[0] += 3;
        correction[3] += 2;
    }

    if (jumps >=15)
    {
        correction[2] -= 2;
        correction[1] -= 1;
    }
    else if(jumps >=12 && jumps<15)
    {
        correction[2] -= 1;
    }
    else if (jumps >=8 && jumps<12)
    {
        correction[2] += 1;
    }
    else
    {
        correction[2] += 2;
        correction[1] += 1;
    }

    //winpercentage means how close to winning they were
    if(winPercentage>= 0.8)
    {
        correction[0] += 2;
        correction[3] += 2;
        correction[2] += 1;
        correction[1] += 1;
    }
    else if(winPercentage>=0.6 && winPercentage<0.8)
    {
        correction[0] += 1;
        correction[2] += 1;
    }
    else if(winPercentage>=0.4 && winPercentage <0.6)
    {
        correction[0] -= 1;
        correction[2] -= 1;
    }
    else
    {
        correction[0] -= 2;
        correction[3] -= 1;
        correction[2] -= 1;
        correction[1] -= 1;
    }
    
    System.out.println("Correction: ");
    for (int i = 0; i<correction.length; i++ )
    {
        //if(correction[i] <= 0)
        //{
        //    correction[i] = 1;
        //}

        System.out.println(correction[i]);
    }

    saveStats();
    stats.clear();
    //return parameterDiff;

    return correction;
}

    //critic level generated performance
public double[] critic(double[] difficulties)
{
    double[] noCorrection = {};
    double[] correction ={1,1,1,1};
    // score their performance based on stats and average stats
    int scoreDistance = 10;
    int scoreKills = 10;
    //int scoreCoins = 10;
    int jumps = 10;
    //int actions = 0;
    //int jumpFreq;

    for (HashMap.Entry<Integer,Integer[]> stat : stats.entrySet() )
    {

        //implement avg distance of ten seconds critc path (reduce enemy line and cannon, reduce tubes)
        //win percentage closer to winning means increase more difficult if lower reduce
        if(stat.getKey() <10)
        {
            scoreDistance += stat.getValue()[0] - ((avgDistance*stat.getKey())/10);
            scoreKills += stat.getValue()[1] - ((avgKills*stat.getKey())/10);
            //actions += stat.getValue()[3];
            jumps += stat.getValue()[4] - ((avgJumps*stat.getKey())/10);
        }
        else
        {

            scoreDistance += stat.getValue()[0] - avgDistance;
            scoreKills += stat.getValue()[1] - avgKills;
            //actions += stat.getValue()[3];
            jumps += stat.getValue()[4] - avgJumps;
            //TO DO - compute action over distance covered every ten seconds to determine actions perfromed
        }

    }
    //jumpFreq = jumps/actions;

    //change magnitude of certain stats to 30 and score performance over 100
    //scoreDistance = (scoreDistance * 30 )/ 20;
    //scoreActions = (scoreActions * 30) / 20;

    //add base case for negative diffiulty
    //add win or death
    //or check if its acc necessar

    
    //2nd parameter for adjusting the odds of cannons spawning
    //3rd parameter for increasing or decreasing number and difficulty of enemy
    if(scoreDistance >= 15)
    {
        correction[0] += 2;
        correction[1] += 1;
        correction[2] += 2;
        correction[3] += 2;
    }
    else if(scoreDistance >= 12 && scoreDistance < 15)
    {
        correction[0] += 1;
        correction[1] += 1;
        correction[2] += 1;
    }
    else if(scoreDistance >= 8 && scoreDistance < 12)
    {
        correction[0] += 1;
    }
    else
    {
        correction[0] -= 1;
        correction[1] -= 1;
        correction[2] -= 1;
    }

    if (scoreKills >= 12  && scoreKills<15)
    {
        correction[0] += 2;
        correction[3] += 2;
    }
    else if (scoreKills >= 8  && scoreKills<12)
    {
        correction[0] += 2;
    }
    else if(scoreKills<8 && wonLevel)
    {
        correction[0] += 2;
    }
    else if (scoreKills<8)
    {
        correction[0] -= 1;
    }
    else if (scoreKills >= 15 )
    {
        correction[0] += 3;
        correction[3] += 2;
    }

    if (jumps >=15)
    {
        correction[2] -= 2;
        correction[1] -= 1;
    }
    else if(jumps >=12 && jumps<15)
    {
        correction[2] -= 1;
    }
    else if (jumps >=8 && jumps<12)
    {
        correction[2] += 1;
    }
    else
    {
        correction[2] += 2;
        correction[1] += 1;
    }

    //winpercentage means how close to winning they were
    if(winPercentage>= 0.8)
    {
        correction[0] += 2;
        correction[3] += 2;
        correction[2] += 1;
        correction[1] += 1;
    }
    else if(winPercentage>=0.6 && winPercentage<0.8)
    {
        correction[0] += 1;
        correction[2] += 1;
    }
    else if(winPercentage>=0.4 && winPercentage <0.6)
    {
        correction[0] -= 1;
        correction[2] -= 1;
    }
    else
    {
        correction[0] -= 2;
        correction[3] -= 1;
        correction[2] -= 1;
        correction[1] -= 1;
    }
    
    System.out.println("Correction: ");
    for (int i = 0; i<correction.length; i++ )
    {
        //if(correction[i] <= 0)
        //{
        //    correction[i] = 1;
        //}

        System.out.println(correction[i]);
    }

    saveStats();
    stats.clear();
    //return parameterDiff;

    //calculate where or not to correct the NN
    double diff = 0;
    for(int i = 0; i<correction.length;i++)
    {
        diff += Math.abs(correction[i]-difficulties[i]);
    }

    if(diff<0.3)
    {
        return noCorrection;
    }
    else
    {
        return correction;
    }
}

}
