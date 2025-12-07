
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.Socket;
import java.util.Scanner;

public class ClientHandler extends Thread {

    Socket socket;
    String film;
    byte[] buffer;

    public ClientHandler(Socket socket){
        this.socket = socket;
        buffer = new byte[4096];
    }

    @Override
    public void run(){
        try{
            System.out.println("cleint");
            BufferedInputStream bis = new BufferedInputStream(socket.getInputStream());
            BufferedOutputStream bos = new BufferedOutputStream(socket.getOutputStream());
            Scanner in = new Scanner(bis);
            String message = in.nextLine();
            System.out.println(message);
            buffer = new byte[4096];
            film = message;
            File file = new File("film/esempio.ts");
            //bos.write(message.getBytes(), 0, message.getBytes().length); 
            //bos.flush();
            //socket.shutdownOutput(); //IMPORTANTE
            //socket.close(); 
            FileInputStream fis = new FileInputStream(file);
            int read;

            while ((read = fis.read(buffer)) != -1){
                bos.write(buffer, 0, read);
            }
            bos.flush();
            fis.close();
            socket.shutdownOutput();  
            socket.close();
            
        } catch (Exception a){
            System.err.println(a);
        }
    }

}
