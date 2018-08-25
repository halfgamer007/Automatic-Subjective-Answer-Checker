package predictor;

import java.sql.*;
import javax.swing.*;
import javax.swing.table.*;
import java.awt.*;
import java.awt.event.*;

public class MyClass extends JFrame
{
    JLabel l;
    JTextField t;
    JButton b,b2;
    JTable jt;
    JScrollPane jsp;
    DefaultTableModel dtm;
    
    MyClass()
    {
        Font fn = new Font("Arial", 5, 30);
        l = new JLabel("Student Name : ");
        l.setFont(fn);
        t = new JTextField(15);
        t.setFont(fn);
        b = new JButton("Find");
        b.setFont(fn);
        b2 = new JButton("Logout");
        b2.setFont(fn);
        dtm = new DefaultTableModel();
        jt = new JTable(dtm);
        jsp = new JScrollPane(jt);
        
        JPanel jp = new JPanel(new GridLayout(1,4));
        jp.add(l); jp.add(t); jp.add(b); jp.add(b2);
        
        Container c = getContentPane();
        c.add(jp, BorderLayout.NORTH); 
        c.add(jsp);
        
        try
        {
            Class.forName("com.mysql.jdbc.Driver");
            
            Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3307/predictor","root","mysql@123");
            
            Statement st = con.createStatement();
            
            ResultSet rs1 = st.executeQuery("Select * From Student_Details");
            
            ResultSetMetaData rsmd = rs1.getMetaData();
            
            for(int i=1; i<=rsmd.getColumnCount(); i++)
            {
                dtm.addColumn(rsmd.getColumnName(i));
            }
            
            while(rs1.next())
            {
                Object[] data = new Object[7];
                
                for(int i=0; i<rsmd.getColumnCount(); i++)
                {
                    data[i] = rs1.getString(i+1);
                }
                
                dtm.addRow(data);
            }
                        
            b.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae)
                  
            {
                
                 String std_name = t.getText();
                 
                 
                    int kt=0;
                    int ut=0;
                    int attendence=0;
                    int dist=0;
                    String sinc="";
                    int count=0;
                    
                try
                {
                    ResultSet rs2 = st.executeQuery("Select * From Student_Details WHERE name='"+std_name+"'");

                    while(rs2.next())
                    {
                        kt = rs2.getInt("no_of_kt");
                        ut = rs2.getInt("UT_percent");
                        attendence = rs2.getInt("attendance_percent");
                        dist = rs2.getInt("dist_from_home");
                        sinc = rs2.getString("sincerity");
                    }
                    
                    Prediction p = new Prediction();
                    
                    p.setVisible(true);
                    p.setTitle("Student Details");
                    p.setLocation(300,100);
                    p.setSize(500,400);
                    p.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);                    
                    p.l1.setText("Student Name : " + std_name);
                    
                    if(kt>5)
                    {
                        p.l2.setText("Drop Expectation : Yes");
                        p.l3.setText("No. of KT's : " + kt);
                    }
                    else if(ut<40)
                    {
                        p.l2.setText("Drop Expectation : Yes");
                        p.l3.setText("Unit Test Percentage : " + ut);
                    }
                    else
                    {
                        if(kt > 3)
                            count++;
                        if((sinc.equals("Average")) || (sinc.equals("Poor")))
                            count++;
                        if(dist > 50)
                            count++;
                        if(ut < 50)
                            count++;
                        if(attendence < 50)
                            count++;
                        
                       
                    }
                    
                    if(count<3 && kt<=3 && ut>40 )
                     p.l8.setText("Drop Expectation : No");
                   
                     
                     if(count >= 3)
                    {
                        p.l2.setText("Drop Expectation : Yes");
                        
                        if(kt > 3)
                            p.l3.setText("No of KT's : " + kt);
                        
                        if((sinc.equals("Average")) || (sinc.equals("Poor")))
                            p.l4.setText("Sinceretiy : " + sinc);
                        
                        if(dist > 50)
                            p.l5.setText("Distance From Home : " + dist);
                        
                        if(ut < 50)
                            p.l6.setText("Unit Test Percentage : " + ut);
                        
                        if(attendence < 50)
                            p.l7.setText("Attendence : " + attendence);
                        
                    }
                    
                        
                         
                        
                            
                }
                catch(Exception e)
                {
                    JOptionPane.showMessageDialog(null,"Error : "+e);
                }
            }
            });            
        }
        catch(Exception e)
        {
            JOptionPane.showMessageDialog(null,"Error : "+e);
        }
        
        b2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae)
            {
                Login l = new Login();
                l.setVisible(true);
                l.setSize(400,220);
                l.setLocation(500, 300);
                        
                setVisible(false);
            }
        });
    }
}