package com.ms_service;

import android.accessibilityservice.AccessibilityServiceInfo;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.provider.Settings;
import android.view.accessibility.AccessibilityManager;

import java.util.List;

import androidx.annotation.RequiresApi;

/**
 * device boot receiver
 *
 * @author majh
 */
public class DeviceBootReceiver extends BroadcastReceiver {
//开机启动
    private static final String ACTION_BOOT = "android.intent.action.BOOT_COMPLETED";
    //亮屏启动
//    ACTION_SCREEN_ON
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals(ACTION_BOOT)) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if(isCanDrawOverlays(context) && isAccessibilityServiceEnable(context)) {
                    launchAccessibility(context);
                }else {
                    MainPageGo(context);
                }
            }else {
                if(isAccessibilityServiceEnable(context)) {
                    launchAccessibility(context);
                }else {
                    MainPageGo(context);
                }
            }
        }
    }

    private void MainPageGo(Context context) {
        Intent launch = new Intent(context,MainActivity.class);
        launch.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        context.startActivity(launch);
    }
    public static void launchAccessibility(Context context) {
        Intent intent = new Intent(context, listenservice.class);
        context.startService(intent);
    }

    public static boolean isAccessibilityServiceEnable(Context context) {
        AccessibilityManager accessibilityManager =
                (AccessibilityManager) context.getSystemService(Context.ACCESSIBILITY_SERVICE);
        assert accessibilityManager != null;
        List<AccessibilityServiceInfo> accessibilityServices =
                accessibilityManager.getEnabledAccessibilityServiceList(
                        AccessibilityServiceInfo.FEEDBACK_ALL_MASK);
        for (AccessibilityServiceInfo info : accessibilityServices) {
            if (info.getId().contains(context.getPackageName())) {
                return true;
            }
        }
        return false;
    }
    @RequiresApi(api = Build.VERSION_CODES.M)
    public static boolean isCanDrawOverlays(Context context) {
        return Settings.canDrawOverlays(context);
    }
}
