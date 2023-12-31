# Understanding android virtual device in recipes.

AVD is how flutter launches emulators as defined by CIPD.

* The dependency can be found in https://chrome-infra-packages.appspot.com/p/chromium/tools/android/avd/linux-amd64/
    * Available dependencies appear to be automatically uploaded once per week by the chrome team.
    * At the time of writing, flutter pins the version of avd used.
    * The "versions" supported for a particular dependency come from the source/tools/android/ave/proto directory of the downloaded asset. There is no other way to know support via the CIPD tooling.
* To update the CIPD dependency change AVD_CIPD_IDENTIFIER in [api.py](api.py) to the Instance ID of the desired dependency version, which you may find by clicking on any of the available dependency instances.