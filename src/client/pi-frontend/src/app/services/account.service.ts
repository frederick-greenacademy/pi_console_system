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
  private isCompleteEnrollSubject: BehaviorSubject<boolean>;
  public isCompleteEnroll: Observable<boolean>;

  enrollInfo: Account
  capturedImages: File[] = []

  constructor(
    private http: HttpClient) {
      this.isCompleteEnrollSubject = new BehaviorSubject(false)
      this.isCompleteEnroll = this.isCompleteEnrollSubject.asObservable()

  }

  enroll(acc: Account) {
    this.enrollInfo = acc
  }

  register() {
    let formUploadFiles = new FormData()
    let lengthOfImages = this.capturedImages.length
    formUploadFiles.append('number_image_files', lengthOfImages.toString())

    for (let index = 0; index < lengthOfImages; index++) {
      formUploadFiles.append('files[]', this.capturedImages[index], 'file' + index + '.jpg')
    }

    this.uploadFiles(formUploadFiles)
  }

  addCapturedImage(image: File) {
    this.capturedImages.push(image)
    console.log('Trang thai cua isCompleteEnroll: ', this.capturedImages.length >= 6 ? true : false)
    this.isCompleteEnrollSubject.next(this.capturedImages.length >= 6 ? true : false)
  }

  private uploadFiles(formUploadFiles: FormData) {

    let headers = new HttpHeaders()
    headers.append('Content-Disposition', 'multipart/form-data');
    headers.append('Access-Control-Allow-Origin', '*');
    
    this.http.post<any>(this.urlForUploadFiles, formUploadFiles, { headers: headers }).subscribe(
      res => {
        console.log('Phản hồi của tệp tải lên:', res)
      },
      (err) => {
        console.log('Lỗi khi tải tệp lên:', err)
      })
  }
}
