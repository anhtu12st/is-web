import { useState, useRef } from 'react';
import Styled from './styled';
import axios from 'axios'
import { ClipLoader } from 'react-spinners'



export function HomePage() {
  const [image, setImage] = useState(null);
  const [fileImage, setFileImage] = useState(null);
  const [b664img, setImgString] = useState(null);
  const inputImage = useRef(null);
  const [loading, setLoading] = useState(false);
  const handleOnUploadImage = event => {
    if (event.target.files && event.target.files[0]) {
      let img = event.target.files[0];
      setFileImage(img)
      setImage(URL.createObjectURL(img));
    }
  }

  const handleOnClickUploadButton = event => {
    inputImage.current.click();
  }

  const handleCNNDetect = () => {

    const fd = new FormData();
    fd.append('image', fileImage);
    setLoading(true);
    axios.post('http://localhost:5500/detectCNN', fd)
      .then(res => {
        setLoading(false)
        setImgString(res['data']);
      });

  }

  const handleSVMDetect = () => {
    const fd = new FormData();
    fd.append('image', fileImage);
    setLoading(true);
    axios.post('http://localhost:5500/detectSVM', fd)
      .then(res => {
        setLoading(false);
        setImgString(res['data']);
      });
  }


  return (
    <Styled.AppContainer>
      <Styled.ImagesContainer>
        <div style={{ flexBasis: "40%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <img src={image} alt="image" />
        </div>

        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20 }}>
          <Styled.Button onClick={handleCNNDetect}>CNN Detect</Styled.Button>
          <Styled.Button onClick={handleSVMDetect}>SVM Detect</Styled.Button>
        </div>

        <div style={{ flexBasis: "40%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          {loading ? <ClipLoader color="#4A90E2" loading={loading} size={50} /> : <img src={"data:image/png;base64," + b664img} alt="image" />}

        </div>
      </Styled.ImagesContainer>
      <input style={{ display: 'none' }} ref={inputImage} type="file" onChange={handleOnUploadImage} placeholder="Load Image" />
      <Styled.Button onClick={handleOnClickUploadButton}>Load Image</Styled.Button>
      <div>
        <div>Camera IP</div>
        <div style={{ width: 320, fontSize: 30, height: 60, border: '1px solid black', borderRadius: 8, textAlign: 'center', lineHeight: '60px' }}>
          01.01.01.01
        </div>
      </div>
      <Styled.CameraButtonContainer>
        <Styled.Button>Connect Camera</Styled.Button>
        <Styled.Button>Stop</Styled.Button>
      </Styled.CameraButtonContainer>
    </Styled.AppContainer>
  );
}
