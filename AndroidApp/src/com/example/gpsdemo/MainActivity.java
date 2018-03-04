package com.example.gpsdemo;

import java.util.List;
import java.util.Locale;

import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.app.ProgressDialog;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;


public class MainActivity extends Activity {
	Button btn1,btn2;
	TextView gps,net;
	Location locg,locn;
	LocationManager lm;
	ProgressDialog pd;
	String address;
	Geocoder geocoder;
    int i;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		btn1=(Button) findViewById(R.id.button1);
		btn2=(Button) findViewById(R.id.button2);
		gps=(TextView) findViewById(R.id.textView1);
		net=(TextView) findViewById(R.id.textView2);
		lm=(LocationManager) getSystemService(LOCATION_SERVICE);
		btn1.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				locg=lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
				locn=lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
				if(locg!=null)
				{
				  Double lat_g,lon_g;
				  lat_g=locg.getLatitude();
				  lon_g=locg.getLongitude();
				  gps.setText(""+lat_g+"\n"+lon_g);
				  	}
				else
				{
					gps.setText("NO DATA..");
				}
				if(locn!=null)
				{
				  Double lat_n,lon_n;
				  lat_n=locn.getLatitude();
				  lon_n=locn.getLongitude();
				  net.setText(""+lat_n+"\n"+lon_n);
				  	}
				else
				{
					net.setText("NO DATA..");
				}
			}
		});
		btn2.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				new MyAddress().execute();
			}
		});
	}
	public class MyAddress extends AsyncTask<String, String, String>
	{

		@Override
		protected String doInBackground(String... arg0) {
			// TODO Auto-generated method stub
		if(locg!=null)
		{
			address=getAddress(locg.getLatitude(),locg.getLongitude());
					
		}
			return null;
		}
	private String getAddress(double latitude,double longitude)
	{
		geocoder=new Geocoder(MainActivity.this,Locale.ENGLISH);
     	String ret;
		try
		{
			List<Address> addresses=geocoder.getFromLocation(latitude, longitude, 1);
			if(addresses!=null)
			{
				Address returnaddress=addresses.get(0);
				StringBuilder strreturnaddress=new StringBuilder("Address: \n");
						for(i=0;i<returnaddress.getMaxAddressLineIndex();i++)
						{
							strreturnaddress.append(returnaddress.getAddressLine(i)).append("\n");
						}
						ret=strreturnaddress.toString();
			}
			else
			{
				ret="No Address Found";
			}
		}
			catch(Exception e)
			{
				e.printStackTrace();
				ret="Can't get Address";
			}
			return ret;
		}
		
		protected void onPostExecute(String result){
			super.onPostExecute(result);
			pd.dismiss();
			gps.setText(""+address);
		}
	
		protected void onPreExecute(){
			super.onPreExecute();
			pd=new ProgressDialog(MainActivity.this);
			pd.setMessage("Please wait..");
			pd.show();
		
	}
}

	}
	


