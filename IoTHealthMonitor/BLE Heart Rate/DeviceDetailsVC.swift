//
//  DeviceDetailsVC.swift
//  Remote Health Monitoring
//
//  Created by Anuj Patel on 5/3/17.
//  Copyright © 2017 Anuj Patel. All rights reserved.
//

import  UIKit
import Foundation
import CoreBluetooth
import Alamofire

class DeviceDetailsVC: UIViewController,CBCentralManagerDelegate, CBPeripheralDelegate {

    var selectedDeviceUUID:String = ""
    let BLEServiceHeartRate = "180D"
    let BLECharacteristicsHeartRate = "2A37"
    var manager:CBCentralManager!
    var polarHeartRateMonitor:CBPeripheral!
    var timer = Timer()
    var userID:String = "" 
    var smsBody:String = ""
    
    
        var emergencyName:String = ""
        var emergencyEmail:String = ""
        var emergencyPhone:String = ""
        var emergencyPhone2:String = ""
        var emergencyUserID:String = ""
        var emergencyAddress:String = ""
        var emergencyRelationship:String = ""
    
    
    
    @IBOutlet weak var bluetoothStatusLabel: UILabel!
    
    @IBOutlet weak var deviceNameLabel: UILabel!
    
    @IBOutlet weak var heartRateLabel: UILabel!
    
    @IBOutlet weak var bpmLabel: UILabel!
    
    override func viewDidLoad() {
        print("This is the selected device UUID\(selectedDeviceUUID)")
        manager = CBCentralManager(delegate: self, queue: nil)
        timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(DeviceDetailsVC.postHeartRateToServer), userInfo: nil, repeats: true)
        
        print("User ID in Device detail is  \(userID)")
        getEmergencyContacts()
    }



    // This is the REST Function used to post data
    func data_request(_ url:String, _heartRateValue:String)
        
    {
        let url:NSURL = NSURL(string:url)!
        let session = URLSession.shared
        
        let request = NSMutableURLRequest(url:url as URL)
        request.httpMethod = "POST"
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        
        
        
        let timestamp = NSDate().timeIntervalSince1970
        let date = Date(timeIntervalSince1970: timestamp)
        let dateFormatter = DateFormatter()
        dateFormatter.timeZone = TimeZone(abbreviation: "PST") //Set timezone that you want
        dateFormatter.locale = NSLocale.current
        dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss" //Specify your format that you want
        let strDate = dateFormatter.string(from: date)
        
        
        
        let json: [String: Any] = ["userId":Int(userID),"heartRate":  (_heartRateValue), "timestamp": (strDate)]
        
        let jsonData = try? JSONSerialization.data(withJSONObject: json)
        
        
        request.httpBody = jsonData
        
        let task = session.dataTask(with: request as URLRequest){
            (
            data,response,error) in
            
            guard let _:NSData = data as NSData?, let _:URLResponse = response, error == nil else{
                print("error")
                return
            }
            
        }
        
        
        task.resume()
        
        
        
        //Checking for alerts
       if _heartRateValue != ""{
        let heartRateInt:Int = Int(_heartRateValue)!
        print("Hear Rate in Int \(heartRateInt)")
        
        if (heartRateInt > 30 && heartRateInt < 75){
            print("Sending Low heart rate alert. Heart rate:\(heartRateInt) BPM")
            smsBody = "Heart rate is very low at \(heartRateInt) BPM. Please check if everything is ok."
            sendAlertSMS()
        } else if (heartRateInt > 120){
            print("Sending High heart rate alert. Heart rate:\(heartRateInt) BPM")
            smsBody = "Heart rate is very high at \(heartRateInt) BPM. Please check if everything is ok."
            sendAlertSMS()
        }
        
        
        }
        
        
        
        
        
    }
    
    
    
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        
        print("Peripheral Detected: \(peripheral.name!)")
        deviceNameLabel.text = peripheral.name!
        bpmLabel.text = "BPM"
            if (("\(peripheral.identifier)") == selectedDeviceUUID){
            self.polarHeartRateMonitor = peripheral
            self.polarHeartRateMonitor.delegate = self
            manager.stopScan()
            manager.connect(self.polarHeartRateMonitor, options: nil)
        }
    }
    
    
    func postHeartRateToServer(){
        print("Posting to Server")
        print(" \(heartRateLabel.text!) BPM")
        data_request("http://requestb.in/13x5x9d1", _heartRateValue: heartRateLabel.text!)
        data_request("http://34.223.225.244:8080/heartratelive/webapi/heartrate", _heartRateValue: heartRateLabel.text!)
        
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
    
    
    
    func update(heartRateData:Data){
        print("Updating Heart Rate...")
        var buffer = [UInt8](repeating: 0x00, count: heartRateData.count)
        heartRateData.copyBytes(to: &buffer, count: buffer.count)
        
        var bpm:UInt16?
        if (buffer.count >= 2){
            if (buffer[0] & 0x01 == 0){
                bpm = UInt16(buffer[1]);
            }else {
                bpm = UInt16(buffer[1]) << 8
                bpm =  bpm! | UInt16(buffer[2])
                print("\(bpm) BPM")
            }
        }
        
        if let actualBpm = bpm{
            heartRateLabel.text = ("\(actualBpm)")
            print("\(actualBpm) BPM")
            
            
        }else {
            
            print(bpm!)
        }
    }
    
    
    
    // Will send data to server when there is a new value
    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        print("--- didUpdateValueForCharacteristic")
        
        if (error) != nil{
            
        }else {
            switch characteristic.uuid.uuidString{
            case "2A37":
                update(heartRateData:characteristic.value!)
                
                
            default:
                print("--- something other than 2A37 uuid characteristic")
            }
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
        bluetoothStatusLabel.text = consoleMessage
    }
    
    
    // Send Alert SMS
    func sendAlertSMS(){
        print("=====Sending SMS Alert To Emergency Contacts=====")
        let headers = [
            "Content-Type": "application/x-www-form-urlencoded"
        ]
        
        let parameters: Parameters = [
            "To": "\(emergencyPhone)",
            "Body": "\(smsBody)"
        ]
        
        Alamofire.request("54.69.139.242:5000/sms", method: .post, parameters: parameters, headers: headers).response { response in
            print(response)
            print("Parameters are:\(parameters)")
            
        }
    }
    
    
    
    func getEmergencyContacts(){
  // Sending Get request to collect list of Emergency contacts
    
        
        
        Alamofire.request("http://54.69.139.242:3000/emergencyContactsMobile?userId=\(userID)", method: .get).responseJSON
    {
    response in
    //printing response
    print(response)
    
    //getting the json value from the server
    if let result = response.result.value {
    
    //converting it as NSDictionary
    let jsonData = result
    
    if let array = jsonData as? [[String: Any]] {
    print(array)
    
    if let firstObject = array.first {
    // access individual object in array
    print("=====Printing Emergency Contact Details=====")
    
    for (key, value) in firstObject {
    // access all key / value pairs in dictionary
    
    
    if key == "Name"{
    print("\(key): \(value)")
        self.emergencyName = "\(value)"
        print("\(key): \(value)")
    } else if key == "Email"{
        self.emergencyEmail = "\(value)"
        print("\(key): \(value)")
    } else if key == "Phone"{
        self.emergencyPhone = "+1\(value)"
        print("\(key): +1\(value)")
    } else if key == "Phone2"{
        self.emergencyPhone2 = "+1\(value)"
        print("\(key): \(value)")
    } else if key == "Relation"{
        self.emergencyRelationship = "\(value)"
        print("\(key): +1\(value)")
    } else if key == "Address"{
        self.emergencyAddress = "\(value)"
        print("\(key): \(value)")
    }
    
    }
    
    }
    }
    }
    }
    
    
   }
    
    
    
    
    
    
    
    
    

}
