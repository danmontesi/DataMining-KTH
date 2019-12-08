package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class Jabeja {
  final static Logger logger = Logger.getLogger(Jabeja.class);
  private final Config config;
  private final HashMap<Integer/*id*/, Node/*neighbors*/> entireGraph;
  private final List<Integer> nodeIds;
  private int numberOfSwaps;
  private int round;

  private float T;
  private boolean resultFileCreated = false;
  private int roundRestart = 400;


  //-------------------------------------------------------------------
  public Jabeja(HashMap<Integer, Node> graph, Config config) {
    this.entireGraph = graph;
    this.nodeIds = new ArrayList(entireGraph.keySet());
    this.round = 0;
    this.numberOfSwaps = 0;
    this.config = config;
    this.T = config.getTemperature();
  }


  //-------------------------------------------------------------------
  public void startJabeja() throws IOException {
    for (round = 0; round < config.getRounds(); round++) {
      for (int id : entireGraph.keySet()) {
        sampleAndSwap(id);
      }
        //TODO TASK 2: restart; every roundRestart round add a restart. N defined by config
        if (roundRestart>0) {
            if (round % roundRestart == 0) {
                this.T = config.getTemperature();
            }
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
  private void saCoolDown(){
    // FIRST implementation (already present)
/*
    if (this.T > 1)
      this.T -= config.getDelta();
    if (this.T < 1)
      this.T = 1;

*/

  // TODO Task 2: change tMin (very small) and Tstart (max 1)
      float tMin = 0.001f;
    if (this.T > tMin) {
        this.T = T - config.getDelta() - T*config.getDelta();;
        if (this.T < tMin) System.out.println("\n\n\nReached Tmin\n\n\n");
    }
    if (this.T < tMin)
          this.T = tMin;

/*
    //Third task completion: paper on http://katrinaeg.com/simulated-annealing.html
      // Set Tmin and put T_new = T_old*talpha. with talpha <1 and close to 1.
      // If T<Tmin -> set T to Tmin

    float tMin = 0.00001f;
    float alphaT = config.getTAlpha();

    this.T = this.T*alphaT;
    if (this.T <= tMin)
      this.T = tMin;
*/

  }


  /**
   * Sample and swap algorithm at node p
   * @param nodeId
   */
  private void sampleAndSwap(int nodeId) {
    Node partner = null;
    Node nodep = entireGraph.get(nodeId);

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL) {
      // swap with random neighbors
      partner = findPartner(nodeId, getNeighbors(nodep));
    }

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM) {
      // if local policy fails then randomly sample the entire graph
      if(partner == null)
        partner = findPartner(nodeId, getSample(nodeId));
    }

    // swap the colors
    if(partner != null){
      int thisColor = nodep.getColor();
      nodep.setColor(partner.getColor());
      partner.setColor(thisColor);
      numberOfSwaps++;
    }

  }

  public double calculateAcceptanceProbability(double oldCost, double newCost){
      // Math.pow(Math.E, (oldCost - newCost) / T)) is 1 when acceptance must be LOW (inverse) -> let's do
    double acc = Math.pow(Math.E, (oldCost - newCost) / T);
    if (acc >1) acc=1;
    return acc;
  }

  public Node findPartner(int nodeId, Integer[] nodes){

    Node nodep = entireGraph.get(nodeId);

    Node bestPartner = null;

    // Task1
    double highestBenefit = 0;

    double lowestCost = Math.pow(10, 10);

    for (Integer node:nodes) {
        Node nodeq = entireGraph.get(node);

        // Task 1
/*
        int dpp = getDegree(nodep, nodep.getColor());
        int dqq = getDegree(nodeq, nodeq.getColor());

        // dpp dqq
        double oldValue = (Math.pow(dpp, config.getAlpha()) + Math.pow(dqq, config.getAlpha()));
        int dpq = getDegree(nodep, nodeq.getColor());
        int dqp = getDegree(nodeq, nodep.getColor());
        // dpq dqp
        double newValue = (Math.pow(dpq, config.getAlpha()) + Math.pow(dqp, config.getAlpha()));
        // Task 1


      if(newValue*this.T > newValue && newValue > highestBenefit){
        bestPartner = nodeq;
        highestBenefit = newValue;
      }
    }
*/

        // TODO Task 2: introduce an acceptProbability calculated based on the old/new cost difference

        // Oss: the cost is how much we "pay" and we want to minimize it. Here instead we have a "value" instead of the cost
        // for this reason, we calculate a "Cost" as the number of degrees of a nodes - number of neighbors of its colours. (cost of maintaining old solution)

        // Get the costs
        int qDegreeDiff = getNeighbors(nodeq).length - getDegree(nodeq, nodeq.getColor());
        int pDegreeDiff = getNeighbors(nodep).length - getDegree(nodep, nodep.getColor());

        int qDegreePCol = getNeighbors(nodeq).length - getDegree(nodeq, nodep.getColor());
        int pDegreeQCol = getNeighbors(nodep).length - getDegree(nodep, nodeq.getColor());

        // the new alpha favorites the OldCost when higher than newCost. Alpha should hence be
        double oldCost = (Math.pow(qDegreeDiff, config.getAlpha()) + Math.pow(pDegreeDiff, config.getAlpha()));
        double newCost = (Math.pow(qDegreePCol, config.getAlpha()) + Math.pow(pDegreeQCol, config.getAlpha()));

        Random random = new Random();

        double acceptProbability = this.calculateAcceptanceProbability(oldCost, newCost);

        double r = random.nextDouble();

        if ((newCost < lowestCost) && (acceptProbability > r)) {
            bestPartner = nodeq;
            lowestCost = newCost;
        }

    }

    return bestPartner;
  }

  /**
   * The the degreee on the node based on color
   * @param node
   * @param colorId
   * @return how many neighbors of the node have color == colorId
   */
  private int getDegree(Node node, int colorId){
    int degree = 0;
    for(int neighborId : node.getNeighbours()){
      Node neighbor = entireGraph.get(neighborId);
      if(neighbor.getColor() == colorId){
        degree++;
      }
    }
    return degree;
  }

  /**
   * Returns a uniformly random sample of the graph
   * @param currentNodeId
   * @return Returns a uniformly random sample of the graph
   */
  private Integer[] getSample(int currentNodeId) {
    int count = config.getUniformRandomSampleSize();
    int rndId;
    int size = entireGraph.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    while (true) {
      rndId = nodeIds.get(RandNoGenerator.nextInt(size));
      if (rndId != currentNodeId && !rndIds.contains(rndId)) {
        rndIds.add(rndId);
        count--;
      }

      if (count == 0)
        break;
    }

    Integer[] ids = new Integer[rndIds.size()];
    return rndIds.toArray(ids);
  }

  /**
   * Get random neighbors. The number of random neighbors is controlled using
   * -closeByNeighbors command line argument which can be obtained from the config
   * using {@link Config#getRandomNeighborSampleSize()}
   * @param node
   * @return
   */
  private Integer[] getNeighbors(Node node) {
    ArrayList<Integer> list = node.getNeighbours();
    int count = config.getRandomNeighborSampleSize();
    int rndId;
    int index;
    int size = list.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    if (size <= count)
      rndIds.addAll(list);
    else {
      while (true) {
        index = RandNoGenerator.nextInt(size);
        rndId = list.get(index);
        if (!rndIds.contains(rndId)) {
          rndIds.add(rndId);
          count--;
        }

        if (count == 0)
          break;
      }
    }

    Integer[] arr = new Integer[rndIds.size()];
    return rndIds.toArray(arr);
  }


  /**
   * Generate a report which is stored in a file in the output dir.
   *
   * @throws IOException
   */
  private void report() throws IOException {
    int grayLinks = 0;
    int migrations = 0; // number of nodes that have changed the initial color
    int size = entireGraph.size();

    for (int i : entireGraph.keySet()) {
      Node node = entireGraph.get(i);
      int nodeColor = node.getColor();
      ArrayList<Integer> nodeNeighbours = node.getNeighbours();

      if (nodeColor != node.getInitColor()) {
        migrations++;
      }

      if (nodeNeighbours != null) {
        for (int n : nodeNeighbours) {
          Node p = entireGraph.get(n);
          int pColor = p.getColor();

          if (nodeColor != pColor)
            grayLinks++;
        }
      }
    }

    int edgeCut = grayLinks / 2;

    logger.info("round: " + round +
            ", edge cut:" + edgeCut +
            ", swaps: " + numberOfSwaps +
            ", migrations: " + migrations);

    saveToFile(edgeCut, migrations);
  }

  private void saveToFile(int edgeCuts, int migrations) throws IOException {
    String delimiter = "\t\t";
    String outputFilePath;

    //output file name
    File inputFile = new File(config.getGraphFilePath());
    outputFilePath = config.getOutputDir() +
            File.separator +
            inputFile.getName() + "_" +
            "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
            "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
            "T" + "_" + config.getTemperature() + "_" +
            "D" + "_" + config.getDelta() + "_" +
            "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
            "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
            "A" + "_" + config.getAlpha() + "_" +
            "R" + "_" + config.getRounds() + ".txt";

    if (!resultFileCreated) {
      File outputDir = new File(config.getOutputDir());
      if (!outputDir.exists()) {
        if (!outputDir.mkdir()) {
          throw new IOException("Unable to create the output directory");
        }
      }
      // create folder and result file with header
      String header = "# Migration is number of nodes that have changed color.";
      header += "\n\nRound" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations" + delimiter + "Skipped" + "\n";
      FileIO.write(header, outputFilePath);
      resultFileCreated = true;
    }

    FileIO.append(round + delimiter + (edgeCuts) + delimiter + numberOfSwaps + delimiter + migrations + "\n", outputFilePath);
  }
}
