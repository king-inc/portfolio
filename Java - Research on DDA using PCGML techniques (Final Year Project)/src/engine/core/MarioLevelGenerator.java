package engine.core;

public interface MarioLevelGenerator {
    /**
     * Generate a playable mario level
     *
     * @param model contain a model of the level
     */
    String getGeneratedLevel(MarioLevelModel model, MarioTimer timer);
    String getGeneratedLevel(MarioLevelModel model, MarioTimer timer, double[] difficulties);

    /**
     * Return the name of the level generator
     *
     * @return the name of the level generator
     */

    int getDifficulty();
    String getGeneratorName();
}
