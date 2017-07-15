//
//  AlertTableViewController.swift
//  Remote Health Monitoring
//
//  Created by Anuj Patel on 5/7/17.
//  Copyright © 2017 Anuj Patel. All rights reserved.
//

import Foundation
import UIKit



class AlertTableViewCell:UITableViewCell{
    
    @IBOutlet weak var alertIcon: UIImageView!
    @IBOutlet weak var alertDeviceName: UILabel!
    @IBOutlet weak var alertDate: UILabel!
    
}

class AlertTableViewController: UIViewController, UITableViewDelegate, UITableViewDataSource{

    @IBOutlet weak var alertTable: UITableView!
    
    
    var alertDict:Dictionary = [String: String]()
    var key:String = ""
    var value:String = ""
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        alertDict["04/27/2017 09:14 PM"] = "Polar H7 CEC33E13"
    }
    
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! AlertTableViewCell
        
        
        
        // Storing date as key and device name as value
        key   = Array(self.alertDict.keys)[indexPath.row]
        value = Array(self.alertDict.values)[indexPath.row]
        
        
        
        cell.alertDeviceName.text = "\(value)"
        cell.alertDate.text = "\(key)"
        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return alertDict.count
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.performSegue(withIdentifier: "alertDetail", sender: nil)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "alertDetail"{
            
        let AlertsDetailsVC = segue.destination as! AlertsDetailsVC
            
//            print(AlertsDetailsVC.alertDetailDate.text!)
//            
//            
//            AlertsDetailsVC.alertDetailDateString = key
//            AlertsDetailsVC.alertDetailDeviceString = value
//            AlertsDetailsVC.alertDetailMessageString = "This is a test"

        }
        
    }
    
    
    
}
