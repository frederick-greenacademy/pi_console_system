import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { first } from 'rxjs/operators';
import { ApiHandlerService } from './services/api-handler.service';
import {Account} from './models/account'
import { from } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'pi-frontend';
  user: Account
  constructor(
    private router: Router,
    private apiHandler: ApiHandlerService
  ) {
    this.apiHandler.currentUser.subscribe( u => {
      if(u) {
        this.user = u
        this.router.navigate(['/home']);
      } else {
        this.router.navigate(['/login']);
      }
    })
  }

  logout() {
    this.apiHandler.logout()
    this.router.navigate(['/login']);
  }
} 
