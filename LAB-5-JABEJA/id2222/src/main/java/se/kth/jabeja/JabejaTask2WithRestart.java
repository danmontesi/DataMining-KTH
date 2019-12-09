package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;

import java.io.IOException;
import java.util.HashMap;
import java.util.Random;

public class JabejaTask2WithRestart extends JabejaTask2{
  private int roundRestart = 80;
  private int firsRestart = 200;


  //-------------------------------------------------------------------
  public JabejaTask2WithRestart(HashMap<Integer, Node> graph, Config config) {
    super(graph, config);
    config.setRounds(10000);
  }


  //-------------------------------------------------------------------
  public void startJabeja() throws IOException {
    for (round = 0; round < config.getRounds(); round++) {
      for (int id : entireGraph.keySet()) {
        sampleAndSwap(id);
      }
        if (roundRestart>0 && round >= firsRestart) {
            if (round % roundRestart == 0) {
                this.T = config.getTemperature();
                this.config.setDelta(this.config.getDelta()/this.config.getTAlpha());
            }
        }
      //one cycle for all nodes have completed.
      //reduce the temperature
      saCoolDown();
      report();
    }
  }
}
