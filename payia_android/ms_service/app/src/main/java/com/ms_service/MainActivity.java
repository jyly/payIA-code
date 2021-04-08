package com.ms_service;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.AppOpsManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends AppCompatActivity {
    private static final int ACCESSIBILITY_REQUEST_CODE = 438;
    Button login;
    EditText userid;
    String user;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        permissionrequest();
        userid = (EditText) findViewById(R.id.userid);
        login = (Button) findViewById(R.id.sign_in);
        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                user = userid.getText().toString();
                if (user.equals("")) {
                    Toast.makeText(MainActivity.this, "请输入用户账号。", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(MainActivity.this, "开始监听后台程序。", Toast.LENGTH_SHORT).show();
                    writefile(user);
                    finish();
                }
            }
        });
    }
    public void writefile(String userid) {
        String readfile = getExternalFilesDir("").getAbsolutePath() + "readername.txt";//文件存储路径
        File prereader;
        try {
            prereader = new File(readfile);
            prereader.delete();
            prereader.createNewFile();
            FileOutputStream os = new FileOutputStream(prereader, true);
            StringBuilder sb = new StringBuilder();
            sb.append(userid);
            os.write(sb.toString().getBytes());
            os.flush();
            os.close();
        } catch (Exception e) {
        }
    }

    private void permissionrequest() {
        getprimePermission();
        getflatwindowvisible();
//        finish();
    }




    private void getprimePermission() {
        //弹窗权限访问
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:" + getPackageName()));
//                startActivityForResult(intent, 5004);
                startActivity(intent);
//                Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION);
//                startActivityForResult(intent, FLAT_REQUEST_CODE);
            }
        }
    }

    private void getflatwindowvisible() {
        //辅助功能权限开启
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            // > M,grant permission
            if (!DeviceBootReceiver.isAccessibilityServiceEnable(this)) {
                Intent accessibleIntent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
                startActivityForResult(accessibleIntent, ACCESSIBILITY_REQUEST_CODE);
            }
        }
    }
}
