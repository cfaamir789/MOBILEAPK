package com.mobileapk;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        TextView titleText = findViewById(R.id.titleText);
        TextView versionText = findViewById(R.id.versionText);
        TextView descText = findViewById(R.id.descText);
        
        titleText.setText("MOBILEAPK");
        versionText.setText("Version 1.0");
        descText.setText("Welcome to the Mobile APK demo application! This app demonstrates a simple Android application structure.");
    }
}
