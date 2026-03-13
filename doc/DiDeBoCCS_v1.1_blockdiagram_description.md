

Top level structure: 8 components: Powerbank, BeagleBoneWithFoccciCape, UserInterface (consisting of Display and Button), StepUp, MeasurementBoard, HvConnections, CommunicationConnection, PowerSwitch.

The BeagleBoneWithFoccciCape is the central element. The Powerbank supplies 5V via PowerSwitch to BeagleBoneWithFoccciCape, Display, StepUp, MeasurementBoard.

The Display gets the data via CAN bus from the BeagleBoneWithFoccciCape.

The Button connects to BeagleBoneWithFoccciCape.

The StepUp gets 5 discrete signals from BeagleBoneWithFoccciCape for voltage control.

The MeasurementBoard sends one analog signal 0 to 5V to the BeagleBoneWithFoccciCape.

The HvConnections has the lines DC+ and DC- and both are linked to the MeasurementBoard and StepUp.

The CommunicationConnection is linked to the BeagleBoneWithFoccciCape via lines CP and PE.

The StepUp drives the DC lines.

The StepUp has a voltage range of 0 to 410V DC.

The MeasurementBoard measures the voltage on the DC lines.

Both the MeasurementBoard and the StepUp are galvanically isolated. The isolation is inside the MeasurementBoard and StepUp.

The StepUp consists of 5 groups of isolated DCDC converters. For each of the following voltages: 225V, 100V, 50V, 25V, 12V.

The groups are connected in series on HV side, to get the sum voltage. On LV side, each group is controlled from the related discrete line via a FET, that switches the ground connection of the group.

The HV domain contains a BulbInterface. Inside the BulbInterface there is a FET, a Relay and BananaSockets. The Relay is fed by DC+/DC- from the HvConnections. The Relay is driven via a discrete line from the BeagleBoneWithFoccciCape. 
