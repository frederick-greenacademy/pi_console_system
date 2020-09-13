import { Injectable } from '@angular/core';
import { from } from 'rxjs';
import { HttpClient } from '@angular/common/http'
import { HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { map } from 'rxjs/operators';
import { Account } from '../models/account'

@Injectable({
  providedIn: 'root'
})
export class AccountHandler {

  private urlForUploadFiles = 'http://192.168.0.101:8000/upload/files'
  enrollInfo: Account
  imageProfile: File[]

  constructor(
    private http: HttpClient) {

  }

  enroll(acc: Account) {
    this.enrollInfo = acc
  }

  register() {
    
  }

  uploadFiles(formData: FormData) {
    var headers = new HttpHeaders()
    headers.append('Content-Disposition', 'multipart/form-data');
    headers.append('Access-Control-Allow-Origin', '*');

    this.http.post<any>(this.urlForUploadFiles, formData, { headers: headers }).subscribe(
      res => {
        console.log('Phản hồi của tệp tải lên:', res)
      },
      (err) => {
        console.log('Lỗi khi tải tệp lên:', err)
      })
  }
}
