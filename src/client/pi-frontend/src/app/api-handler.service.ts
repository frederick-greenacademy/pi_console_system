import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from "rxjs";
import { catchError, retry } from "rxjs/operator";

@Injectable({
  providedIn: 'root'
})

export class ApiHandlerService {

  constructor(private http: HttpClient) {

  }
}
