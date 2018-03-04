using Android.App;
using Android.Widget;
using Android.OS;
using Android.Locations;
using System.Collections.Generic;
using Android.Util;
using System.Linq;
using Android.Runtime;
using System.Timers;
using System;
using System.Net;
using System.IO;
using HttpUtils;

namespace GPSUpdater
{
	[Activity(Label = "GPSUpdater", MainLauncher = true, Icon = "@mipmap/icon")]
	public class MainActivity : Activity, ILocationListener
	{
		protected override void OnCreate(Bundle savedInstanceState)
		{
			base.OnCreate(savedInstanceState);

			// Set our view from the "main" layout resource
			SetContentView(Resource.Layout.Main);
			
			this.serverURL = FindViewById<EditText>(Resource.Id.serverUrl);
			this.location = FindViewById<TextView>(Resource.Id.locationOutput);

			Button selectServer = FindViewById<Button>(Resource.Id.selectServer);
			selectServer.Click += delegate { this.server = this.serverURL.Text; };

			this.updateGPS = new Timer();
			updateGPS.Interval = 5000;
			updateGPS.Elapsed += sendGPSToServer;
			updateGPS.Enabled = true;

			this.InitializeLocationManager();
		}

		void InitializeLocationManager()
		{
			locationManager = (LocationManager)GetSystemService(LocationService);
			Criteria criteriaForLocationService = new Criteria
			{
				Accuracy = Accuracy.Fine
			};
			IList<string> acceptableLocationProviders = locationManager.GetProviders(criteriaForLocationService, true);

			if (acceptableLocationProviders.Any())
			{
				locationProvider = acceptableLocationProviders.First();
			}
			else
			{
				locationProvider = string.Empty;
			}
			Log.Debug(MainActivity.TAG, "Using " + locationProvider + ".");
		}

		public void OnLocationChanged(Location location)
		{
			this.gpsPosition = location;
			this.location.Text = location.Latitude + "," + location.Longitude;
		}

		public void OnProviderDisabled(string provider)
		{
			return; //do nothing
		}

		public void OnProviderEnabled(string provider)
		{
			return; //do nothing
		}

		public void OnStatusChanged(string provider, [GeneratedEnum] Availability status, Bundle extras)
		{
			return; //do nothing
		}

		protected override void OnResume()
		{
			base.OnResume();
			this.locationManager.RequestLocationUpdates(this.locationProvider, 0, 0, this);
		}

		private void sendGPSToServer(object sender, ElapsedEventArgs e)
		{
			if (this.gpsPosition != null && this.server != "")
			{
				try
				{
					var client = new RestClient(endpoint: "http://" + this.server + "/cgi-bin/getpage.cgi",
						method: HttpVerb.GET);
					var result = client.MakeRequest("?action=updategps&lat=" + this.gpsPosition.Latitude + "&long=" + this.gpsPosition.Longitude);
				}
				catch (Exception)
				{
					//do nothing
				}
			}
		}

		LocationManager locationManager;
		TextView location;
		EditText serverURL;
		Location gpsPosition;
		string locationProvider;
		string server;
		Timer updateGPS;

		static readonly string TAG = "X:" + typeof(MainActivity).Name;
	}
}

