import { Component, OnInit } from '@angular/core';
import { ApiHandlerService } from '../services/api-handler.service';
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

  constructor(private apiHandler: ApiHandlerService) {
    this.apiHandler.currentUser.subscribe(u => {
      this.user = u
    })
  }

  ngOnInit(): void {
  }


}
