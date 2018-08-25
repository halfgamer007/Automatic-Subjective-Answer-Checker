package predictor;

import java.sql.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class SignUp extends JFrame
{
    JLabel l1,l2;
    JTextField t1;
    JPasswordField p1;
    JButton b1;
    
    SignUp()
    {
        Font fn = new Font("Arial", 5, 30);
        l1 = new JLabel("Username : ");
        l1.setFont(fn);
        l2 = new JLabel("Password : ");
        l2.setFont(fn);
        t1 = new JTextField(15);
        t1.setFont(fn);
        p1 = new JPasswordField(15);
        b1 = new JButton("SignUp");
        b1.setFont(fn);
        
        Container c = getContentPane();
        
        JPanel jp = new JPanel(new GridLayout(2,2));
         
        jp.add(l1); jp.add(t1);
        jp.add(l2); jp.add(p1);
        c.add(jp);
        c.add(b1, BorderLayout.SOUTH);
                
        b1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae)
            {
                
                String username = t1.getText();        
                String password = p1.getText();
               
                // Checks whether username & password field are empty or not 
                if(username.trim().length()<1 || password.trim().length()<1)
                {
                    JOptionPane.showMessageDialog(null, "Plz Enter Valid Username & Password");
                    t1.setText(""); 
                    p1.setText("");
                }
                else
                {
                try
                {
                    Class.forName("com.mysql.jdbc.Driver");
                    
                    Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3307/predictor","root","mysql@123");
                    
                    PreparedStatement ps = con.prepareStatement("Insert into Login values(?,?)");
                    
                    ps.setString(1,username);
                    ps.setString(2,password);
                    
                    ps.execute();
                    
                    JOptionPane.showMessageDialog(null, "Signed Up Successfully...");  
                    
                    Login l = new Login();
                    l.setVisible(true);
                    l.setSize(300,300);
                    
                    setVisible(false);
                }
                catch(Exception e)
                {
                    JOptionPane.showMessageDialog(null, "Error : " + e);
                }
                }
            }
        });
    }
}