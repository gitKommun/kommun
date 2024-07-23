from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from members.models import User
from documents.models import Folder, Document
from django.core.files.uploadedfile import SimpleUploadedFile

class FolderAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register-main-contact-community')
        self.login_url = reverse('user-login')
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "name": "Test",
            "surnames": "User"
        }
        
        # User registration
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # User login
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.csrf_token = response.cookies['csrftoken'].value
        self.sessionid = response.cookies['sessionid'].value
        self.client.cookies['csrftoken'] = self.csrf_token
        self.client.cookies['sessionid'] = self.sessionid

        self.user = User.objects.get(email=self.user_data['email'])
        self.community = self.user.current_community

    def test_create_folder(self):
        print("Testing folder creation")
        url = reverse('folder_create_api', kwargs={'IDcommunity': self.community.IDcommunity})
        data = {
            'name': 'Test Folder'
        }
        response = self.client.post(url, data, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Folder')
        print("Folder creation validated")

    def test_get_folder_detail(self):
        print("Testing get folder detail")
        folderL1 = Folder.objects.create(
            name='Folder L1',
            community=self.community,
            parent_folder_id=0
        )
        folderL2 = Folder.objects.create(
            name='Subfolder L2',
            community=self.community,
            parent_folder_id=folderL1.folder_id
        )
        Document.objects.create(
            name='Document 1',
            community=self.community,
            folder_id=folderL1.folder_id,
        )
        url = reverse('folder_detail_api', kwargs={'IDcommunity': self.community.IDcommunity, 'IDfolder': folderL1.folder_id})
        response = self.client.get(url, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['folders'][0]['folder_id'], folderL2.folder_id)
        self.assertEqual(response.data['folders'][0]['name'], 'Subfolder L2')
        self.assertEqual(response.data['path'][0]['folder_id'], 0)
        self.assertEqual(response.data['path'][0]['name'], 'root')
        self.assertEqual(response.data['path'][1]['folder_id'], folderL1.folder_id)
        self.assertEqual(response.data['path'][1]['name'], 'Folder L1')
        print("Get folder detail validated")

    def test_delete_folder(self):
        print("Testing folder deletion")
        folder = Folder.objects.create(
            name='Folder to Delete',
            community=self.community,
            parent_folder_id=0
        )
        url = reverse('folder_delete_api', kwargs={'IDcommunity': self.community.IDcommunity, 'IDfolder': folder.folder_id})
        response = self.client.delete(url, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Folder.objects.filter(folder_id=folder.folder_id).exists())
        print("Folder deletion validated")

    def test_update_folder(self):
        print("Testing folder update")
        folder = Folder.objects.create(
            name='Folder to Update',
            community=self.community,
            parent_folder_id=None
        )
        url = reverse('folder_update_api', kwargs={'IDcommunity': self.community.IDcommunity, 'IDfolder': folder.folder_id})
        data = {
            'name': 'Updated Folder Name'
        }
        response = self.client.put(url, data, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        folder.refresh_from_db()
        self.assertEqual(folder.name, 'Updated Folder Name')
        print("Folder update validated")

    
    def test_upload_document(self):
        print("Testing document upload")
        folder = Folder.objects.create(
            name='Folder for Document',
            community=self.community,
            parent_folder_id=0
        )
        url = reverse('documents-upload', kwargs={'IDcommunity': self.community.IDcommunity, 'IDfolder': folder.folder_id})
        
        # Create sample file
        file = SimpleUploadedFile("file1.pdf", b"file_content1", content_type="application/pdf")
        data = {
            'file': [file]
        }
        
        response = self.client.post(url, data, format='multipart', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'file1.pdf')
        print("Document upload validated")

    def test_upload_multiple_documents(self):
        print("Testing multiple document upload")
        folder = Folder.objects.create(
            name='Folder for Multiple Documents',
            community=self.community,
            parent_folder_id=0
        )
        url = reverse('documents-upload', kwargs={'IDcommunity': self.community.IDcommunity, 'IDfolder': folder.folder_id})

        # Create sample files
        files = [
            SimpleUploadedFile("file1.pdf", b"file_content1", content_type="application/pdf"),
            SimpleUploadedFile("file2.pdf", b"file_content2", content_type="application/pdf"),
            SimpleUploadedFile("file3.pdf", b"file_content3", content_type="application/pdf"),
        ]
        data = {
            'file': files
        }
        
        response = self.client.post(url, data, format='multipart', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'file1.pdf')
        self.assertEqual(response.data[1]['name'], 'file2.pdf')
        self.assertEqual(response.data[2]['name'], 'file3.pdf')
        print("Multiple document upload validated")

    def test_download_document(self):
        print("Testing document download")
        folder = Folder.objects.create(
            name='Folder for Download',
            community=self.community,
            parent_folder_id=0
        )
        document = Document.objects.create(
            name='Document to Download',
            community=self.community,
            folder_id=folder.folder_id,
            file=SimpleUploadedFile("file_to_download.pdf", b"file_content_download", content_type="application/pdf")
        )
        url = reverse('document-download', kwargs={'IDcommunity': self.community.IDcommunity, 'IDdocument': document.document_id})
        response = self.client.get(url, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data[0]['name'], 'Document to Download')
        print("Document download validated")

    def test_delete_document(self):
        print("Testing document deletion")
        folder = Folder.objects.create(
            name='Folder for Document Deletion',
            community=self.community,
            parent_folder_id=0
        )
        document = Document.objects.create(
            name='Document to Delete',
            community=self.community,
            folder_id=folder.folder_id,
            file=SimpleUploadedFile("file_to_delete.pdf", b"file_content_delete", content_type="application/pdf")
        )
        url = reverse('document-delete', kwargs={'IDcommunity': self.community.IDcommunity, 'IDdocument': document.document_id})
        response = self.client.delete(url, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(document_id=document.document_id).exists())
        print("Document deletion validated")
