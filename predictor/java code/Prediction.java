package predictor;

import javax.swing.*;
import java.awt.*;

public class Prediction extends JFrame
{
    JLabel l1,l2,l3,l4,l5,l6,l7,l8;
    
    Prediction()
    {
        Font fn = new Font("Arial", 5, 30);
        l1 = new JLabel();
        l1.setFont(fn);
        l2 = new JLabel();
        l2.setFont(fn);
        l3 = new JLabel();
        l3.setFont(fn);
        l4 = new JLabel();
        l4.setFont(fn);
        l5 = new JLabel();
        l5.setFont(fn);
        l6 = new JLabel();
        l6.setFont(fn);
        l7 = new JLabel();
        l8 = new JLabel();
        l7.setFont(fn);
        
        Container c = getContentPane();
        c.setLayout(new FlowLayout());
        
        c.add(l1); c.add(l2); c.add(l3);
        c.add(l4); c.add(l5); c.add(l6); c.add(l7);
        c.add(l8);
    }
}