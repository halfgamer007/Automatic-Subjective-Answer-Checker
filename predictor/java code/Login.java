package predictor;

import java.sql.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Login extends JFrame
{
    JLabel l1,l2;
    JTextField t1;
    JButton b1,b2;
    JPasswordField  p;
    
    Login()
    {
        Font fn = new Font("Arial", 5, 30);
        l1 = new JLabel("User ID ");
        l1.setFont(fn);
        l2 = new JLabel("Password ");
        l2.setFont(fn);
        t1 = new JTextField(15);
        t1.setFont(fn);
        b1 = new JButton("Login"); 
        b1.setFont(fn);
        b2 = new JButton("Sign Up");
        b2.setFont(fn);
        p = new JPasswordField(15);
        
        // We cannot manipulate or edit the JFrame so we use the Container class
        Container c = getContentPane();
        
        // Setting layout as grid layout with 3 rows & 2 columns
        c.setLayout(new GridLayout(3,2));
        c.add(l1); c.add(t1);
        c.add(l2); c.add(p);
        c.add(b1); c.add(b2);
        
        b1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae)
            {
                try
                {            
                    // Creating Connection Bridge with MySQL
                    Class.forName("com.mysql.jdbc.Driver");
                    
                    // Creating Connection Between Java & MySql
                    Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3307/predictor","root","mysql@123");
                    
                    // For creating & executing SQL query
                    Statement st = con.createStatement();
                    
                    // Store the query result
                    ResultSet rs = st.executeQuery("Select * From Login");
                    
                    String username = t1.getText();
                    String password = p.getText();
                    
                    // while loop will iterate untill pointer reaches the last record or last row
                    while(rs.next())
                    {
                        if((username.equals(rs.getString(1))) && (password.equals(rs.getString(2))))
                        {
                            JOptionPane.showMessageDialog(null,"Logged In Successfully");
                    
                            MyClass mc = new MyClass();
                            mc.setVisible(true);
                            mc.setTitle("Predictor");
                            mc.setSize(700,500);
                            mc.setLocation(300, 100);
                            mc.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);   
                            setVisible(false);
                            
                            break;
                        }
                        else
                        {
                            JOptionPane.showMessageDialog(null,"Invalid Username & Password");
                        }
                    }
                }
                catch(Exception e)
                {
                    JOptionPane.showMessageDialog(null,"Error : "+e);
                }
            }
        });
        
        b2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae)
            {
                SignUp su = new SignUp();
                su.setVisible(true);
                su.setLocation(500,200);
                su.setSize(400,200);
                su.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                
                setVisible(false);
            }
        });
    }
    
    public static void main(String args[])throws Exception
    {
        Login l = new Login();
        l.setTitle("Login");
        l.setVisible(true);
        l.setSize(400,220);
        l.setLocation(500, 300);
        l.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}
