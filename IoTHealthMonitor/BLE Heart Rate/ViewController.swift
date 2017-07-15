//
//  ViewController.swift
//  BLE Heart Rate
//
//  Created by Anuj Patel on 2/27/17.
//  Copyright © 2017 Anuj Patel. All rights reserved.
//

import UIKit
import CoreBluetooth


class MyCustomTableViewCell:UITableViewCell{
    @IBOutlet weak var deviceNameLabel: UILabel!
    @IBOutlet weak var deviceStatusColor: UIImageView!
    @IBOutlet weak var deviceStatusLabel: UILabel!
}


class ViewController: UIViewController, CBCentralManagerDelegate, CBPeripheralDelegate, UITableViewDelegate, UITableViewDataSource{
    
    @IBOutlet weak var tableView: UITableView!
    
    var userIDListVC:String = ""
    
    let BLEServiceHeartRate = "180D"
    let BLECharacteristicsHeartRate = "2A37"
    var selectedRow:String = ""
    var key:String = ""
    var value:String = ""
    var peripheralsDict:Dictionary = [String: String]()
    
    
    var manager:CBCentralManager!
    var polarHeartRateMonitor:CBPeripheral!
    var timer = Timer()
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        manager = CBCentralManager(delegate: self, queue: nil)
    print("User ID is \(userIDListVC)")
    
    }
    
    
    
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        
        
        let peripheralName:String? = peripheral.name
        let peripheralState:CBPeripheralState = peripheral.state
        
        if peripheralName != nil{
            tableView.reloadData()
            peripheralsDict["\(peripheral.identifier)"] = "\(peripheralName!)"
        }
        
        
        
        
        print(peripheralsDict)
    }
    
    
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if let servicePeripherals = peripheral.services as [CBService]!
        {
            for service in servicePeripherals{
                
                peripheral.discoverCharacteristics(nil, for: service)
            }
        }
    }
    
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        
        if let characterArray =  service.characteristics as [CBCharacteristic]!
        {
            for cc in characterArray
            {
                if (cc.uuid.uuidString == "2A37"){
                    print("Heart Rate found")
                    peripheral.readValue(for: cc)
                    peripheral.setNotifyValue(true, for: cc)
                }
            }
        }
    }
    
    
    func peripheral(_ peripheral: CBPeripheral, didUpdateNotificationStateFor characteristic: CBCharacteristic, error: Error?) {
        
        if error != nil {
            print("Error changing notification state: \(error?.localizedDescription)")
        }
        // Notification has started
        if characteristic.isNotifying {
            print("Notification began on \(characteristic)")
        }
    }
    

    
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        peripheral.delegate = self
        peripheral.discoverServices(nil)
    }
    
    
    
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        
        var consoleMessage = ""
        
        switch (central.state) {
            
        case .poweredOff:
            consoleMessage = "Powered off"
            
        case .poweredOn:
            consoleMessage = "Powered on"
            
            manager.scanForPeripherals(withServices: [CBUUID.init(string: BLEServiceHeartRate)], options: nil)
            
        case .resetting:
            consoleMessage = "Resetting"
            
        case .unauthorized:
            consoleMessage = "Unauthorized"
            
        case .unknown:
            consoleMessage = "Unknown"
            
        case .unsupported:
            consoleMessage = "Bluetooth LE is unsupported"
            
            
        }
        
        print("\(consoleMessage)")
    }
    
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! MyCustomTableViewCell

         key   = Array(self.peripheralsDict.keys)[indexPath.row]
         value = Array(self.peripheralsDict.values)[indexPath.row]
        
        
        
        cell.deviceNameLabel.text = "\(value)"
        cell.deviceStatusLabel.text = "Available"
        cell.deviceStatusColor.image = #imageLiteral(resourceName: "green_icon.png")
        
        return cell
    }
    
    
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return peripheralsDict.count
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.performSegue(withIdentifier: "deviceDetail", sender: nil)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "deviceDetail"{
            
            let DeviceDetailsVC = segue.destination as! DeviceDetailsVC
            DeviceDetailsVC.selectedDeviceUUID = key
            DeviceDetailsVC.userID = userIDListVC
    }
    
}
}
