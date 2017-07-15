//
//  UserProfileVC.swift
//  Remote Health Monitoring
//
//  Created by Anuj Patel on 5/10/17.
//  Copyright © 2017 Anuj Patel. All rights reserved.
//

import Foundation
import UIKit
import Alamofire

class UserProfileVC: UIViewController {
 
    var userIdProfile:String = ""
    
    @IBOutlet weak var nameLabel: UILabel!
    
    @IBOutlet weak var emailLabel: UILabel!
    
    @IBOutlet weak var genderLabel: UILabel!
    
    @IBOutlet weak var ageTextField: UITextField!
    
    @IBOutlet weak var heightTextField: UITextField!
    
    @IBOutlet weak var weightTextField: UITextField!
    
    
    @IBAction func saveProfileChanges(_ sender: Any) {
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(userIdProfile)
        
        
        
        
        //Sending http get request to fetch profile data
        Alamofire.request("http://54.69.139.242:3000/getUserProfileMobile?userId=\(userIdProfile)", method: .get).responseJSON
            {
                response in
                //printing response
                
                
                //getting the json value from the server
                if let result = response.result.value {
                    
                    //converting it as NSDictionary
                    let jsonData = result

                if let array = jsonData as? [[String: Any]] {
                    

                    if let firstObject = array.first {
                        print("=====Printing User Profile Details=====")
                        
                        
                        for (key, value) in firstObject {
                            // access all key / value pairs in dictionary
                            print("\(key): \(value)")
                        if key == "Name"{
                            self.nameLabel.text = "\(value)"
                            
                        } else if key == "EmailId"{
                            self.emailLabel.text = "\(value)"
                        } else if key == "Gender"{
                            self.genderLabel.text = "\(value)"
                        } else if key == "Age"{
                            self.ageTextField.text = "\(value)"
                        } else if key == "Height"{
                            self.heightTextField.text = "\(value)"
                        } else if key == "Weight"{
                            self.weightTextField.text = "\(value)"
                        }

                        }
                    
                        }
                    }
                }
        }

        
        
        
        
        
        
        
        
}
}

