//
//  SignInViewController.swift
//  Remote Health Monitoring
//
//  Created by Anuj Patel on 5/7/17.
//  Copyright © 2017 Anuj Patel. All rights reserved.
//

import Alamofire
import Foundation
import UIKit

class SignInViewController: UIViewController {
    
//    let URL_USER_REGISTER = "http://10.0.0.28:3000/users/checkmobilelogin"
    let URL_USER_REGISTER = "http://54.69.139.242:3000/users/checkmobilelogin"
    
    var UserValue:String = ""
    
    @IBOutlet weak var usernameTextField: UITextField!
    
    @IBOutlet weak var passwordTextField: UITextField!
    
    @IBOutlet weak var loginButton: UIButton!
    
//    loginButton
    
    
    @IBAction func loginButtonPressed(_ sender: Any) {
        
        let parameters: Parameters=[
            "email":usernameTextField.text!,
            "password":passwordTextField.text!
        ]
        
        //Sending http post request
        Alamofire.request(URL_USER_REGISTER, method: .post, parameters: parameters).responseJSON
            {
                response in
                //printing response
                print(response)
                
                //getting the json value from the server
                if let result = response.result.value {
                    
                    //converting it as NSDictionary
                    let jsonData = result
//                        as! NSDictionary
                    
                    
                    
                    
//                    if let array = jsonData["result"] as? [[String: Any]] {
                    if let array = jsonData as? [[String: Any]] {
                        if let firstObject = array.first {
                            // access individual object in array
                            
                            
                            for (key, value) in firstObject {
                                // access all key / value pairs in dictionary
                                
                                self.UserValue = ("\(value)")
                                print("User Value is \(self.UserValue)")
                                if self.UserValue == "" {
                                    print("Login Failed")
                                }else{
                                    print("Login Successful")
                                    
                                    self.performSegue(withIdentifier: "segueToVC", sender: self.UserValue)
                                    
                                }
                            }
                        }
                    }
                }
            }
        }
        
    
   override func viewDidLoad() {
        super.viewDidLoad()
        
        
    }
    
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "segueToVC"{
            
            
            
            let tabCtrl = segue.destination as! UITabBarController
            let navCtrl = tabCtrl.viewControllers![0]
            let destinationVC = navCtrl as! UINavigationController
            let deviceListVC = destinationVC.viewControllers[0] as! ViewController
            
                print(tabCtrl.viewControllers![1])
            let userVC = tabCtrl.viewControllers![1] as! UserProfileVC
            userVC.userIdProfile = self.UserValue
//            let userProfileVC = userVC.viewControllers[1] as! UserProfileVC
//
//            userProfileVC.
            deviceListVC.userIDListVC = self.UserValue
        }

}
    


}
    
