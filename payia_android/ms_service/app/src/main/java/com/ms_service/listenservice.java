package com.ms_service;

import android.accessibilityservice.AccessibilityService;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Handler;
import android.os.HandlerThread;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.UUID;

public class listenservice extends AccessibilityService {

    int apptag = 3;
    int timetag = 7;

    float token = 99;
    private SensorManager mSensorManager = null;
    Long opentime = null;
    Long closetime = null;
    ArrayList<Float> dataListx = new ArrayList<Float>();
    ArrayList<Float> dataListy = new ArrayList<Float>();
    ArrayList<Float> dataListz = new ArrayList<Float>();
    ArrayList<Integer> datatag = new ArrayList<Integer>();
    //1加速计，2陀螺仪，3线性加速计，4磁感计，5方向计，7应用开启，8打开摄像头，9摄像头关闭
    ArrayList<Long> timestamp = new ArrayList<Long>();

    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Override
    public void onInterrupt() {

    }

    public void onAccessibilityEvent(AccessibilityEvent event) {
        String pkgName = event.getPackageName().toString();
        Log.e(">>>", "pkgName:" + pkgName);

        int eventType = event.getEventType();
        if (pkgName.equals("com.tencent.mm")) {
            if (apptag != 0) {
                dataclear();
                apptag = 0;
                mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
                StartSensorListening();
            }
        } else {
            if (pkgName.equals("com.eg.android.AlipayGphone")) {
                if (apptag != 1) {
                    dataclear();
                    apptag = 1;
                    mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
                    StartSensorListening();
                }
            } else {
                if (!pkgName.equals("com.android.systemui")) {
                    apptag = 3;
                    dataclear();
                }
            }
        }
        Log.e(">>>", "pkgName:" + pkgName);
        Log.e(">>>", "apptag:" + apptag + ",timetag:" + timetag);
        Log.e(">>>", "eventType:" + eventType);

        if (apptag != 3) {
            AccessibilityNodeInfo nodeInfo = getRootInActiveWindow();


            if (nodeInfo != null) {
                List<AccessibilityNodeInfo> list1 = nodeInfo.findAccessibilityNodeInfosByText("QR");
                List<AccessibilityNodeInfo> list2 = nodeInfo.findAccessibilityNodeInfosByText("pay");
                List<AccessibilityNodeInfo> list3 = nodeInfo.findAccessibilityNodeInfosByText("code");
//                List<AccessibilityNodeInfo> list4 = nodeInfo.findAccessibilityNodeInfosByText("proce");
//                List<AccessibilityNodeInfo> list5 = nodeInfo.findAccessibilityNodeInfosByText("transfer");
//                List<AccessibilityNodeInfo> list5 = nodeInfo.findAccessibilityNodeInfosByText("(");

                Log.e(">>>", "list1:" + list1);
                Log.e(">>>", "list2:" + list2);
                Log.e(">>>", "list3:" + list3);
//                Log.e(">>>", "list3:" + list3);
//                Log.e(">>>", "list4:" + list4);
//                Log.e(">>>", "list5:" + list5);
                //微信
                if (apptag == 0) {
                    if (list3.isEmpty()) {
                        if ((timetag == 8)) {
                            timetag = 9;
                            closetime = System.currentTimeMillis();
                            timestamp.add(closetime);
                            dataListx.add(token);
                            dataListy.add(token);
                            dataListz.add(token);
                            datatag.add(timetag);
                        }
                    }
                    if (!list1.isEmpty()) {
                        for (AccessibilityNodeInfo n : list1) {
                            Log.e(">>>", "n1:" + n);
                            CharSequence pagedescription = n.getContentDescription();
                            if (pagedescription != null) {
//                            Log.e(">>>", "pagedescription:" + pagedescription);
//                                if (pagedescription.toString().equals("You are in the page of,QR Code") && timetag == 7) {
//                                    Log.i(">>>", "wechat QR code page");
//                                    timetag = 8;
//                                    //摄像头被使用，进入抬手阶段
//                                    opentime = System.currentTimeMillis();
//                                    timestamp.add(opentime);
//                                    dataListx.add(token);
//                                    dataListy.add(token);
//                                    dataListz.add(token);
//                                    datatag.add(timetag);
//                                }
                            }
                            CharSequence pagetext = n.getText();
                            if (pagetext != null) {
                                if (pagetext.toString().equals("Scan QR code/barcode/Mini Program code") && timetag == 7) {
                                    Log.i(">>>", "wechat QR code page");
                                    timetag = 8;
                                    //摄像头被使用，进入抬手阶段
                                    opentime = System.currentTimeMillis();
                                    timestamp.add(opentime);
                                    dataListx.add(token);
                                    dataListy.add(token);
                                    dataListz.add(token);
                                    datatag.add(timetag);
                                }
                            }
                        }
                    }
                    for (AccessibilityNodeInfo n : list2) {
                        Log.e(">>>", "n2:" + n);
                        CharSequence pagedescription = n.getContentDescription();
                        if (pagedescription != null) {
                            if (pagedescription.toString().equals("You are in the page of,Pay") && ( timetag == 8 || timetag == 9)) {
                                Log.i(">>>", "wechat amount write page");
                                closetime = System.currentTimeMillis();
                                timetag = 19;
                                timestamp.add(closetime);
                                //摄像头使用结束，进入放下阶段
                                dataListx.add(token);
                                dataListy.add(token);
                                dataListz.add(token);
                                datatag.add(timetag);
                            }
                        }
                        CharSequence pagetext = n.getText();
                        if (pagetext != null) {
                            if (pagetext.toString().equals("Payment Method") && (timetag == 19||timetag == 9)) {
                                Log.i(">>>", "wechat pay page");
                                timetag = 10;
                                senddata(apptag);
                            }
                        }
                    }
                }
                //支付宝
                if (apptag == 1) {
                    if (list1.isEmpty()) {
                        if ((timetag == 8)) {
                            timetag = 9;
                            closetime = System.currentTimeMillis();
                            timestamp.add(closetime);
                            dataListx.add(token);
                            dataListy.add(token);
                            dataListz.add(token);
                            datatag.add(timetag);
                        }
                    } else {
                        for (AccessibilityNodeInfo n : list1) {
                            Log.e(">>>", "n1:" + n);
                            CharSequence pagetext = n.getText();
                            Log.e(">>>", "pagetext:" + pagetext);
                            if (pagetext != null) {
                                if (pagetext.toString().equals("Put QR Code within frame to scan") && timetag == 7) {
                                    Log.i(">>>", "alipay QR code page");
                                    timetag = 8;
                                    opentime = System.currentTimeMillis();
                                    timestamp.add(opentime);
                                    //摄像头被使用，进入抬手阶段
                                    dataListx.add(token);
                                    dataListy.add(token);
                                    dataListz.add(token);
                                    datatag.add(timetag);
                                }
                            }
                        }
                    }
                    for (AccessibilityNodeInfo n : list2) {
                        Log.e(">>>", "n2:" + n);
                        CharSequence pagetext = n.getText();
                        if (pagetext != null) {
//                            Log.e(">>>", "pagetext:" + pagetext);
//                            if (pagetext.toString().equals("Forgot password? Retrieve it and complete payment") && (timetag == 9)) {
                                if (pagetext.toString().equals("Payment details") && (timetag == 9|| timetag == 19)) {
                                Log.i(">>>", "alipay pay page");
                                timetag = 10;
                                senddata(apptag);
                            }
                            if (pagetext.equals("Payment is instant and irrevocable") && (timetag == 9 || timetag == 8)) {
                                timetag = 19;
                                closetime = System.currentTimeMillis();
                                timestamp.add(closetime);
                                dataListx.add(token);
                                dataListy.add(token);
                                dataListz.add(token);
                                datatag.add(timetag);
                            }
                        }
                    }
                }
            }
        }

    }


    public String readname() {
        String readfile = getExternalFilesDir("").getAbsolutePath() + "readername.txt";//文件存储路径
        File prereader;
        String user = "0";
        try {
            prereader = new File(readfile);
            BufferedReader br = new BufferedReader(new FileReader(prereader));
            user = br.readLine();
            br.close();

        } catch (Exception e) {
            Log.e(">>>", "" + e);
        }
        return user;
    }

    public void writetimelog(String content) {
        String readfile = getExternalFilesDir("").getAbsolutePath() + "timelog.txt";//文件存储路径
        BufferedWriter out = null;
        try {
            out = new BufferedWriter(
                    new OutputStreamWriter(new FileOutputStream(readfile, true)));
            out.write(content);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (out != null) {
                    out.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void writeerror(String timer, String errorlog) {
        String readfile = getExternalFilesDir("").getAbsolutePath() + "erroe.txt";//文件存储路径
        File prereader;
        try {
            prereader = new File(readfile);
            prereader.delete();
            prereader.createNewFile();
            FileOutputStream os = new FileOutputStream(prereader, true);
            StringBuilder sb = new StringBuilder();
            long times = System.currentTimeMillis();
            sb.append(timer).append(",").append(errorlog);
            os.write(sb.toString().getBytes());
            os.flush();
            os.close();
        } catch (Exception e) {
        }
    }

    private void senddata(int apptag) {

        StopSensorListening();
        HandlerThread thread = new HandlerThread("update");
        thread.start();
        final Handler uHandler = new Handler(thread.getLooper());
        final long uptime = System.currentTimeMillis();
        final int tag = apptag;
        final String timeer = gettimes();
        final String user = readname().replace(" ", "");
        final NotificationUtils noti = new NotificationUtils(getBaseContext());

        uHandler.post(new Runnable() {
            @Override
            public void run() {
                Log.e("cat", ">>>uploadFile");
                final String TAG = "uploadFile";
                String RequestURL = "http://10.128.227.68:8002/IA";
//                String RequestURL = "http://10.128.219.10:8001";
                final int TIME_OUT = 8000;   //超时时间
                final String CHARSET = "utf-8"; //设置编码
                BufferedReader reader = null;
                String BOUNDARY = UUID.randomUUID().toString();  //边界标识   随机生成
                String PREFIX = "--", LINE_END = "\r\n";
                String CONTENT_TYPE = "multipart/form-data";   //内容类型
                try {
                    URL url = new URL(RequestURL);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setReadTimeout(TIME_OUT);
                    conn.setConnectTimeout(TIME_OUT);
                    conn.setDoInput(true);  //允许输入流
                    conn.setDoOutput(true); //允许输出流
                    conn.setUseCaches(false);  //不允许使用缓存
                    conn.setRequestMethod("POST");  //请求方式
                    conn.setRequestProperty("Charset", CHARSET);  //设置编码
                    conn.setRequestProperty("connection", "keep-alive");
                    conn.setRequestProperty("Content-Type", CONTENT_TYPE + ";boundary=" + BOUNDARY);
                    DataOutputStream dos = new DataOutputStream(conn.getOutputStream());
                    StringBuilder sb = new StringBuilder();
                    sb.append(PREFIX);
                    sb.append(BOUNDARY);
                    sb.append(LINE_END);
                    JSONObject data = new JSONObject();

                    data.put("id", user);
                    data.put("time", timeer);
                    data.put("apptag", tag);
                    Log.e("cat", ">>>" + data.toString());
                    sb.append("Content-Disposition: form-data; name=\"sensor\";filename=\"" + data.toString() + "\"" + LINE_END);
                    sb.append("Content-Type: application/octet-stream; charset=" + CHARSET + LINE_END);
                    sb.append(LINE_END);
                    int tempflag = 0;
                    Log.e("cat", ">>>" + datatag.get(0));

                    for (int i = 0; i < datatag.size(); i++) {
                        if ((timestamp.get(i) > closetime + 4000)) {
                            break;
                        }
                        if ((timestamp.get(i) > opentime - 4000)) {
                            sb.append(datatag.get(i)).append(",")
                                    .append(dataListx.get(i)).append(",")
                                    .append(dataListy.get(i)).append(",")
                                    .append(dataListz.get(i)).append(",")
                                    .append(timestamp.get(i)).append(",")
                                    .append("\n");
                        }
                    }
                    Log.e("cat", ">>>" + sb.toString());

                    dos.write(sb.toString().getBytes());
                    dos.write(LINE_END.getBytes());
                    byte[] end_data = (PREFIX + BOUNDARY + PREFIX + LINE_END).getBytes();
                    dos.write(end_data);
                    dos.flush();


                    int res = conn.getResponseCode();
                    Log.e(TAG, "response code:" + res);
                    Log.e(TAG, "request success");
                    InputStream in = conn.getInputStream();
                    reader = new BufferedReader(new InputStreamReader(in));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) response.append(line);
                    JSONObject json = new JSONObject(response.toString());
                    Log.e("cat", ">>>>" + json);
                    JSONArray jsonlogin = json.getJSONArray(user);

                    long downtime = System.currentTimeMillis();
                    String content = user + "," + tag + "," + uptime + "," + downtime + "," + (downtime - uptime) + "\n";
//                    Log.e("logfile>>>", content);


                    writetimelog(content);

                    dataclear();

                    if (jsonlogin.opt(0).toString().equals("true")) {
                        Log.e("cat", ">>>>" + json);
                        conn.disconnect();
                        Log.e("cat", "Notification");
//                        noti.sendNotification("通知", "认证通过");
                        noti.sendNotification("通知", "上传成功");

                    }
                    if (jsonlogin.opt(0).toString().equals("false")) {
                        Log.e("cat", ">>>>" + json);
                        conn.disconnect();
                        Log.e("cat", "Notification");
//                        noti.sendNotification("通知", "认证失败");
                        noti.sendNotification("通知", "上传成功");
                    }
//                    android.os.Process.killProcess(android.os.Process.myPid());
                } catch (MalformedURLException e) {
                    e.printStackTrace();
//                    noti.sendNotification("通知", "上传失败"+e);
                    writeerror(timeer, e.toString());
                } catch (IOException e) {
                    e.printStackTrace();
//                    noti.sendNotification("通知", "上传失败"+e);
                    writeerror(timeer, e.toString());

                } catch (JSONException e) {
                    e.printStackTrace();
//                    noti.sendNotification("通知", "上传失败"+e);
                    writeerror(timeer, e.toString());
                }
            }
        });
    }

    private SensorEventListener listener = new SensorEventListener() {
        @Override
        public void onAccuracyChanged(Sensor sensor, int i) {
        }

        public void onSensorChanged(SensorEvent e) {
            switch (e.sensor.getType()) {
                case Sensor.TYPE_ACCELEROMETER:   //加速度传感器
                    long ta = System.currentTimeMillis();
                    timestamp.add(ta);
                    dataListx.add(e.values[0]);
                    dataListy.add(e.values[1]);
                    dataListz.add(e.values[2]);
                    datatag.add(1);
                    break;
                case Sensor.TYPE_GYROSCOPE:     //陀螺传感器
                    long tg = System.currentTimeMillis();
                    timestamp.add(tg);
                    dataListx.add(e.values[0]);
                    dataListy.add(e.values[1]);
                    dataListz.add(e.values[2]);
                    datatag.add(2);
                    break;
                case Sensor.TYPE_LINEAR_ACCELERATION:   //线性加速度传感器
                    long tla = System.currentTimeMillis();
                    timestamp.add(tla);
                    dataListx.add(e.values[0]);
                    dataListy.add(e.values[1]);
                    dataListz.add(e.values[2]);
                    datatag.add(3);
                    break;
                case Sensor.TYPE_MAGNETIC_FIELD:    //磁场传感器
                    long tm = System.currentTimeMillis();
                    timestamp.add(tm);
                    dataListx.add(e.values[0]);
                    dataListy.add(e.values[1]);
                    dataListz.add(e.values[2]);
                    datatag.add(4);
                    break;
                case Sensor.TYPE_ROTATION_VECTOR:   //方向计传感器
                    long to = System.currentTimeMillis();
                    timestamp.add(to);
                    dataListx.add(e.values[0]);
                    dataListy.add(e.values[1]);
                    dataListz.add(e.values[2]);
                    datatag.add(5);
                    break;
            }
        }
    };

    public void StartSensorListening() {
        //super.onResume();
        //加速度传感器注册监听器
        mSensorManager.registerListener(listener, mSensorManager.getDefaultSensor(
                Sensor.TYPE_GYROSCOPE), SensorManager.SENSOR_DELAY_FASTEST);
        //加速度传感器注册监听器
        mSensorManager.registerListener(listener, mSensorManager.getDefaultSensor(
                Sensor.TYPE_ACCELEROMETER), SensorManager.SENSOR_DELAY_FASTEST);
        //线性加速度传感器注册监听器
        mSensorManager.registerListener(listener, mSensorManager.getDefaultSensor(
                Sensor.TYPE_LINEAR_ACCELERATION), SensorManager.SENSOR_DELAY_FASTEST);
        //磁场传感器注册监听器
        mSensorManager.registerListener(listener, mSensorManager.getDefaultSensor(
                Sensor.TYPE_MAGNETIC_FIELD), SensorManager.SENSOR_DELAY_FASTEST);
        //方向计传感器注册监听器
        mSensorManager.registerListener(listener, mSensorManager.getDefaultSensor(
                Sensor.TYPE_ROTATION_VECTOR), SensorManager.SENSOR_DELAY_FASTEST);
    }

    public void StopSensorListening() {
        mSensorManager.unregisterListener(listener);
        mSensorManager = null;
    }

    private String gettimes() {
        Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH) + 1;
        int day = calendar.get(Calendar.DAY_OF_MONTH);
        int hour = calendar.get(Calendar.HOUR_OF_DAY);
        int minute = calendar.get(Calendar.MINUTE);
        int second = calendar.get(Calendar.SECOND);
        String time = year + "-" + month + "-" + day + "-" + hour + "-" + minute + "-" + second;
        return time;
    }

    public void dataclear() {
        if (mSensorManager != null) {
            StopSensorListening();
        }
        dataListx.clear();
        dataListy.clear();
        dataListz.clear();
        datatag.clear();
        timestamp.clear();
        opentime = null;
        closetime = null;
        timetag = 7;
    }
}
