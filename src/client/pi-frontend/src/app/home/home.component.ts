import { Component, OnInit } from '@angular/core';
import { AuthenticationHandler } from '../services/authentication.service';
import { Account } from '../models/account'
import { from } from 'rxjs';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  // khai bao cac bien
  user: Account

  constructor(private authenHandler: AuthenticationHandler) {
    this.authenHandler.currentUser.subscribe(u => {
      this.user = u
    })
  }

  ngOnInit(): void {
  }


}
