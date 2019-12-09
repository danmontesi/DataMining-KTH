package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public class JabejaTask2 extends Jabeja{

  protected Random random = new Random();

  //-------------------------------------------------------------------
  public JabejaTask2 (HashMap<Integer, Node> graph, Config config) {
    super(graph, config);
    this.random.setSeed(config.getSeed());
    config.setTemperature(1.0f);
    this.T = config.getTemperature();
  }


  //-------------------------------------------------------------------
  public void startJabeja() throws IOException {
    for (round = 0; round < config.getRounds(); round++) {
      for (int id : entireGraph.keySet()) {
        sampleAndSwap(id);
      }
      //one cycle for all nodes have completed.
      //reduce the temperature
      saCoolDown();
      report();
    }
  }

  /**
   * Simulated analealing cooling function
   */
  protected void saCoolDown() {

    float tMin = 0.0001f;
    if (this.T > tMin) {
      this.T = T - config.getDelta();
      if (this.T < tMin) System.out.println("\n\n\nReached Tmin\n\n\n");
    }
    if (this.T < tMin)
      this.T = tMin;
  }


  public double calculateAcceptanceProbability(double oldValue, double newValue){
    double acc = Math.pow(Math.E, (newValue - oldValue - 1) / T);
    return acc;
  }

  public Node findPartner(int nodeId, Integer[] nodes){

    Node nodep = entireGraph.get(nodeId);

    Node bestPartner = null;

    // Task1
    double highestBenefit = 0;


    for (Integer node:nodes) {
      Node nodeq = entireGraph.get(node);

      int dpp = getDegree(nodep, nodep.getColor());
      int dqq = getDegree(nodeq, nodeq.getColor());

      // dpp dqq
      double oldValue = (Math.pow(dpp, config.getAlpha()) + Math.pow(dqq, config.getAlpha()));
      int dpq = getDegree(nodep, nodeq.getColor());
      int dqp = getDegree(nodeq, nodep.getColor());
      // dpq dqp
      double newValue = (Math.pow(dpq, config.getAlpha()) + Math.pow(dqp, config.getAlpha()));
      // Task 1



      double acceptProbability = this.calculateAcceptanceProbability(oldValue, newValue);

      if (acceptProbability >= this.random.nextDouble() && newValue > highestBenefit) {
        bestPartner = nodeq;
        highestBenefit = newValue;
      }
    }


    return bestPartner;
  }

}
