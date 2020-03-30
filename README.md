In order to run the code in this repository, there are a couple things you will need to do first.

# Install system and Python requirements
First run the following:
`./pre-requirements.sh`

This will require sudo privileges to install, and includes the system requirements for the Python database-related 
packages.

Next, to create the conda environment, navigate to the top directory of the module and create the conda environment
with `conda env create -f django_test.yml`. You can hereafter activate this environment with `conda activate cfdb-env`.

Finally, again from the top directory, install `django_test` in editable mode with the following command:
`pip install -e .`

in the home directory. This will let you `import django_test` in Python scripts. 

# Create the PostgreSQL user

* Switch to the `postgres` user with `su - postgres`. Note: `sudo` may be necessary here.  
* Enter the `postgres` command prompt with `psql`.  
* Type `\du` to see the current list of users and their permissions.  
* Create a new user with `CREATE USER superintendent;`. This will be the rw user.  
* Give the user a password with `\password superintendent` and enter the password `almostsummer`.  
* The new users should be visible with `\du`.  
* Create the database `CREATE DATABASE school_db;`.  
* Change the owner of the database `ALTER DATABASE school_db OWNER TO superintendent;`.  
* The new database and owner should be visible now with `\l`.  
* Exit the environment with `\dq`.  
* Exit the `postgres` user with `exit`.

# Generate the database

* Navigate to `django_test`.  
* Run `python manage.py migrate` to create all the tables.




#Project
A collection of experiments meant to address a particular question or issue.

####Fields
`Description::TextField`: A description of the experiment.  
`KeyQuestions::TextField`: Notes on the purpose and intention of the experiment.  
`ProjectConfig::JSONField`: The project configuration.  

####ForeignKeyConstraints
* One-to-many with `Experiment`

#Experiment
An experiment conducted on a sample.

####Fields
`StartTime::DateTimeField`: The start of the experiment.  
`StopTime::DateTimeField`: The time the experiment is finished.  
`Notes::TextField`: Notes about the experiment.  
`DocumenterNotes::JSONField`: Timestamped notes about the experiment.  
`ExperimentConfig::JSONField`: The configuration of the experiment including hyper-parameters.
`Designation:Enum`: A label for the type of experiment e.g. Control.  
`ShotNumber::IntegerField`: The number of shots taken.  

####ForeignKeyConstraints
* Many-to-one with `Project`
* One-to-many with `InstrumentConfig`
* Many-to-one with `User`
* Many-to-many with `Instrument`
* One-to-many with `Data`
* Many-to-many with `Sample`
* Many-to-many with `Experiment`

#User
The user - the one who conducts the experiment and prepares batches of samples.

####Fields
`PrimaryName::CharField`: The primary or first name.  
`Surname::CharField`: The surname.  

####ForeignKeyConstraints
* One-to-many with `Experiment`
* One-to-many with `Batch`

#InstrumentConfig
The state of an instrument during an experiment.

####Fields
`State::JSONField`: The state of the instrument.

####ForignKeyConstraints
* Many-to-one with `Experiment`
* Many-to-one with `Instrument`

#Instrument
An instrument that could be queried or controlled in an experiment.

####Fields
`CodeCreationDate::DateTimeField`: ?  
`Description::TextField`: A description of the experiment.  
`Model::CharField`: A short designation of the type of instrument.  
`SerialNumebr::CharField`: An instrument-specific identifier.  
`Vendor::Enum`: The vendor.  
`Location::CharField`: The last known location of the instrument.  
`Notes::CharField`: Notes.  
`Calibration::JSONField`: A calibration used to process raw data into physical values.  
`Version::IntegerField`: A version of the instrument.  

####ForeignKeyConstraints
* One-to-many with `Configuration`
* Many-to-many with `Experiment`
* One-to-many with `Data`

#Data
A piece of data.

####Fields
`Abscissa::JSONField`: The x-coordinates.  
`Value::FloatField`: The value of the Data.  
`TimeSeries::ArrayField`: If there is a data time-series.  
`DocType::Enum`: A designation describing the type of data that associates with relevant documentation and methods.  

####ForeignKeyConstraints
* One-to-many with `File`
* Many-to-many with `ProcessedData`
* Many-to-one with `Instrument`
* Many-to-one with `Experiment`

#ProcessedData
A piece of processed data, derived from other data.

####Fields
`DocType::Enum`: A designation describing the type of data that associates with relevant documentation and methods.  
`AnalysisMethod::JSONType`: Some indication of how the data was processed.  

####ForeignKeyConstraints
* Many-to-many with `Data`
* One-to-many with `File`

#DataFile
A reference to the storage of data-containing files.

####Fields
`FilePath::CharField`: The filepath.  
`CreationDate::DateTimeField`: ?  
`Pattern::CharField`: A regex pattern.  
`FileType::Enum`: The type of file.  

####ForeignKeyConstraints
* Many-to-one with `ProcessedData`
* Many-to-one with `Data`

#DocumentFile
A reference to the storage of plots, white-papers, write-ups related to experiments.

####Fields
`FilePath::CharField`: The filepath.  
`CreationDate::DateTimeField`: ?  
`Pattern::CharField`: A regex pattern.  
`FileType::Enum`: The type of file.  

####ForeignKeyConstraints
* Many-to-one with `Project`
* Many-to-one with `Experiment`










#Material
A material for use in sample fabrication.

####Fields
`Alt-MaterialID::?`: ?  
`MaterialName::CharField`: The name of the material.  
`Purity::FloatField`:  The percentage purity.  
`FormFactor::ChaField`: The shape of the material.  
`Dimensions::JSONField`: The size of the material.  
`StorageLocation::Enum`: The intended location of the material.  
`QuantityPurchased::FloatField`: The amount of the material purchased.  
`QuantityRemaining::FloatField`: The amount of material left unused.  
`Unit::Enum`: The unit in which the material is measured.  
`DateReceived::DateTimeField`: The date the material was received by the organization after purchase-order.  
`Vendor::Enum`: The material vendor.  
`Order::TextField`:: Information about the purchase-order.  
`LotInfo::CharField`: ?  
`Notes::TextField`: Further notes about this particular material.  

##ForeignKeyConstraints
* One-to-many with `DepositionLayer`
* One-to-many with `LayeredSample`

#LayeredSample
A type of sample which is produced by layering material together.

####Fields
`Alt-SampleID::?`: ?  
`DatePrepared::DateTimeField`: When the sample was prepared.  
`DateUsed::DateTimeField`: ?  
`Format::?`: ?
`Mass::FloatField`: The mass of the sample.  
`Unit::Enum`: The unit of the mass field.  
`Notes::TextField`: Any additional notes about the sample.  

####ForeignKeyConstraints
* One-to-many with `DepositionLayer`
* Many-to-one with `Material`
* Many-to-one with `Batch`
* Many-to-many with `Experiment`

#Batch
A fabrication run resulting in the production of a batch of samples.

####Fields
`BatchType::Enum`: The type of fabrication run.  
`FabricationSite::Enum`: Where the fibraction took place.  
`DatePrepared::DateTimeField`: When the fabrication occurred.  
`Notes::TextField`: Further notes on the fabrication.  

####ForeignKeyConstraints
* One-to-many with `LayeredSample`
* Many-to-one with `User`

#DepositionLayer
A layer of material deposited as part of the fabrication of certain samples.

####Fields
`Thickness::FloatField`: The thickness of the sample.

####ForeignKeyConstraints
* Many-to-one with `LayeredSample`
* Many-to-one with `Material`