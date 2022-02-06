package io.dylanwake.tcp;

import java.net.Socket;
import java.util.Arrays;

/**
 * @author Dylan
 * The client to get target cords from jetson
 */

class Dim3i{
    public int x,y,z;
    public Dim3i(int x, int y, int z){
        this.x = x;
        this.y = y;
        this.z = z;
    }

    @Override
    public String toString() {
        return "Dim3i{" +
                "x=" + x +
                ", y=" + y +
                ", z=" + z +
                '}';
    }
}

public class SegmentService {
    public static byte[] REQUEST_HEADER = {'Q','U','E','R','Y'};
    public static String REQUEST_ADDRESS = "localhost";
    public static int REQUEST_PORT = 8081;
    public static Dim3i getPosition(){
        try{
            Socket sc = new Socket(REQUEST_ADDRESS, REQUEST_PORT);
            sc.getOutputStream().write(REQUEST_HEADER);

            byte[] result = new byte[12];
            sc.getInputStream().read(result,0,12);
            sc.close();
            int x = genInteger(Arrays.copyOfRange(result,0,4));
            int y = genInteger(Arrays.copyOfRange(result,4,8));
            int z = genInteger(Arrays.copyOfRange(result,8,12));
            System.out.println(new Dim3i(x,y,z));
            return new Dim3i(x,y,z);
        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }

    public static int genInteger(byte[] bytes){
        assert(bytes.length==4);
        int out = 0;

        for (int i = 0; i < 4; i++) {
            int n = ((int)bytes[i]) & 0xff;
            n <<= (3-i)*8;
            out += n;
        }
        return out;
    }


    public static void main(String[] args) {
        getPosition();
    }
}
