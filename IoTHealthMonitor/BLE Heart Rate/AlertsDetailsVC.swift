//
//  AlertsDetailsVC.swift
//  Remote Health Monitoring
//
//  Created by Anuj Patel on 4/7/17.
//  Copyright © 2017 Anuj Patel. All rights reserved.
//

import  UIKit
import Foundation

class AlertsDetailsVC: UIViewController{
    
    var alertDetailDeviceString:String = ""
    var alertDetailTypeString:String = "Heart Rate"
    var alertDetailDateString:String = ""
    var alertDetailMessageString:String = ""
    
    @IBOutlet weak var alertDetailDevice: UILabel!
    
    @IBOutlet weak var alertDetailType: UILabel!
    
    @IBOutlet weak var alertDetailDate: UILabel!
    
    @IBOutlet weak var alertDetailMessage: UILabel!
    
    override func viewDidLoad() {
      super.viewDidLoad()
        
        alertDetailDevice.text = alertDetailDeviceString
        alertDetailType.text = alertDetailTypeString
        
        alertDetailDate.text = alertDetailDateString
        alertDetailMessage.text = alertDetailMessageString
        
    }

    
}

