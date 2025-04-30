package DDA;

import java.util.List;

public class Util {
    public static double sigmoid(double in){
        return 1 / (1 + Math.exp(-in));
      }


      public static int round(double num)
      {
          return (int) Math.round(num);
      }
  public static Double meanSquareLoss(List<Double> correctAnswers,   List<Double> predictedAnswers){
  double sumSquare = 0;
  for (int i = 0; i < correctAnswers.size(); i++){
    double error = correctAnswers.get(i) - predictedAnswers.get(i);
    sumSquare += (error * error);
  }
  return sumSquare / (correctAnswers.size());
}

  public static Double norm(Double num)
  {
    return (num-0)/(120-0);
  }
}
