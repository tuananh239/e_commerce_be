// Tạo toolbar element
const toolbar = document.createElement('div');
toolbar.id = 'my-extension-toolbar';
toolbar.innerHTML = `
    <button id="btn1" class="toolbar-btn">Thêm vào giỏ hàng</button>
`;

// Thêm toolbar vào body
document.body.appendChild(toolbar);

// Thêm event listeners cho các nút
document.getElementById('btn1').addEventListener('click', () => {
    let price = "";
    let color = "";
    let number = "";
    let size = "";
    let url = "";
    let name = "";
    let urlImage = "";

    url = window.location.href;

    console.log("start getdata")
    
    const elementsTitle = document.querySelectorAll('.title-content');
    
    // Lấy giá trị thẻ h1 trong phần tử đầu tiên của elementsTitle
    if (elementsTitle.length > 0) {
        const firstTitleElement = elementsTitle[0];
        const h1Element = firstTitleElement.querySelector('h1');
        if (h1Element) {
            name = h1Element.textContent.trim();
        } else {
            console.log('Không tìm thấy thẻ h1 trong phần tử đầu tiên');
        }
    } else {
        console.log('Không tìm thấy elements có class title-content');
    }
    
    const elementsImage = document.querySelectorAll('.ant-image-img.preview-img');
    urlImage = elementsImage[0].src;
    // Lấy tất cả element có CẢ HAI class price-info VÀ currency
    const elementsWithBothClasses = document.querySelectorAll('.price-info.currency');

    elementsWithBothClasses.forEach((element, index) => {
        // Lấy tất cả thẻ span trong element
        const spans = element.querySelectorAll('span');
        
        // Kiểm tra xem có đủ 3 span không
        if (spans.length >= 3) {
            const span2Text = spans[1].textContent.trim(); // Span thứ 2 (index 1)
            const span3Text = spans[2].textContent.trim(); // Span thứ 3 (index 2)

            // Ghép 2 giá trị lại
            const combinedText = span2Text + span3Text;
            
            // Chuyển đổi thành số
            const numericValue = parseFloat(combinedText.replace(/[^\d.-]/g, ''));
            
            // Kiểm tra xem có phải số hợp lệ không
            if (!isNaN(numericValue)) {
                price = numericValue;
            } else {
                console.log(`  ❌ Không thể chuyển đổi thành số hợp lệ`);
            }
        } else {
            console.log(`  ❌ Không đủ 3 span trong element này (chỉ có ${spans.length} span)`);
        }
    });

    const activeElementColor = document.querySelector('.sku-filter-button.active');
    
    // Lấy giá trị của thẻ span có class label-name trong activeElementColor
    if (activeElementColor) {
        const labelSpan = activeElementColor.querySelector('.label-name');
        if (labelSpan) {
            const labelValue = labelSpan.textContent.trim();
            color = labelValue;
        } else {
            console.log('Không tìm thấy span có class label-name trong activeElementColor');
        }
    } else {
        console.log('Không tìm thấy element có class active');
    }

    const elementsNumber = document.querySelectorAll('.expand-view-item');
    
    // // Cách 1: Lặp qua tất cả elementsNumber và tìm input trong mỗi element
    // console.log('=== TÌM INPUT TRONG ELEMENTS NUMBER ===');
    // elementsNumber.forEach((element, index) => {
    //     const inputElement = element.querySelector('.ant-input-number-input');
    //     if (inputElement) {
    //         console.log(`Element ${index + 1}:`, {
    //             inputElement: inputElement,
    //             value: inputElement.value,
    //             element: element
    //         });
    //     } else {
    //         console.log(`Element ${index + 1}: Không tìm thấy input`);
    //     }
    // });
    
    // // Cách 2: Lấy tất cả input elements từ tất cả elementsNumber
    const allInputElements = [];
    elementsNumber.forEach((element) => {
        const inputs = element.querySelectorAll('.ant-input-number-input');

        console.log("inputs", inputs)

        inputs.forEach(input => {

            let value = parseInt(input.value);
            if(!isNaN(value) && value > 0) {
                number = parseInt(value);
                const sizeElement = element.querySelectorAll('.item-label');

                if (price !== "") {
                    console.log({
                        "name": name,
                        "link_product": url,
                        "color": color,
                        "size": sizeElement[0].textContent.trim(),
                        "number": number,
                        "price": price
                    })

                    // Call API để thêm sản phẩm vào giỏ hàng
                    const apiData = {
                        "name": name,
                        "link_product": url,
                        "link_product_image": urlImage, // Cần lấy URL hình ảnh sản phẩm
                        "color": color,
                        "size": sizeElement[0].textContent.trim(),
                        "number": number,
                        "price": price,
                        "note": "",
                        "note_staff": ""
                    };

                    console.log("getdata ok")

                    chrome.storage.local.get("token", (result) => {
                        if(result.token){
                            console.log("result", result)

                          // Lấy JWT token từ localStorage hoặc prompt user
                            let jwtToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2lkIiwiZW1haWwiOiJ4eXpAZ21haWwuY29tIiwibmFtZSI6Inh5eiIsInBob25lX251bWJlciI6IjAxIiwic3RvcmFnZSI6InN0cmluZyIsInByb3ZpbmNlIjoiaGEgbm9pIiwiZGlzdHJpY3QiOiJzdHJpbmciLCJhZGRyZXNzX2RldGFpbCI6InN0cmluZyIsImJhbGFuY2UiOjAuMCwicm9sZSI6IlVTRVIiLCJpYXQiOjE3NTA1Nzk1NTUsImV4cCI6MTc1MDU4MzE1NX0.VQzwlBIsNrWOe3smcTaTrtu9ef7w9udu9nFoy4Lbk-yHOcUMQkEHo13HW0d0A6PTmB4H3Rn8uUC7eS7-H1RxJyOGkuUgVKmO8JXtLh_l7lb86hz_qHH3UUXW_UQNJSywLqMI0Ysl3NQAH3dQ318AJYhN11_5ZbW6pKpGtBpEj5M"

                            // Gọi API
                            fetch('http://localhost:9119/e-commerce/v1.0/cart/add-product', {
                                method: 'POST',
                                headers: {
                                    'accept': 'application/json',
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${result.token}`
                                },
                                body: JSON.stringify(apiData)
                            })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error(`HTTP error! status: ${response.status}`);
                                }
                                else{
                                    console.log("ok")
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log('API Response:', data);
                                
                                // Hiển thị thông báo thành công
                                const successNotification = document.createElement('div');
                                successNotification.style.cssText = `
                                    position: fixed;
                                    top: 20px;
                                    right: 20px;
                                    background: #4CAF50;
                                    color: white;
                                    padding: 15px;
                                    border-radius: 5px;
                                    z-index: 10000;
                                    font-family: Arial, sans-serif;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                                `;
                                successNotification.textContent = `Đã thêm sản phẩm vào giỏ hàng thành công!`;
                                document.body.appendChild(successNotification);
                                
                                // Tự động xóa thông báo sau 3 giây
                                setTimeout(() => {
                                    if (successNotification.parentNode) {
                                        successNotification.parentNode.removeChild(successNotification);
                                    }
                                }, 3000);
                            })
                            .catch(error => {
                                console.error('API Error:', error);
                                
                                // Hiển thị thông báo lỗi
                                const errorNotification = document.createElement('div');
                                errorNotification.style.cssText = `
                                    position: fixed;
                                    top: 20px;
                                    right: 20px;
                                    background: #f44336;
                                    color: white;
                                    padding: 15px;
                                    border-radius: 5px;
                                    z-index: 10000;
                                    font-family: Arial, sans-serif;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                                `;
                                errorNotification.textContent = `Lỗi khi thêm sản phẩm: ${error.message}`;
                                document.body.appendChild(errorNotification);
                                
                                // Tự động xóa thông báo sau 3 giây
                                setTimeout(() => {
                                    if (errorNotification.parentNode) {
                                        errorNotification.parentNode.removeChild(errorNotification);
                                    }
                                }, 3000);
                            });
                        }
                        else{
                            // Hiển thị thông báo lỗi
                            const errorNotification = document.createElement('div');
                            errorNotification.style.cssText = `
                                position: fixed;
                                top: 20px;
                                right: 20px;
                                background: #f44336;
                                color: white;
                                padding: 15px;
                                border-radius: 5px;
                                z-index: 10000;
                                font-family: Arial, sans-serif;
                                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                            `;
                            errorNotification.textContent = `Chưa đăng nhập Extension!`;
                            document.body.appendChild(errorNotification);
                            
                            // Tự động xóa thông báo sau 3 giây
                            setTimeout(() => {
                                if (errorNotification.parentNode) {
                                    errorNotification.parentNode.removeChild(errorNotification);
                                }
                            }, 3000);
                        }
                    });

                    
                    
                }
            }
        });
    });
    
    // // Cách 3: Sử dụng Array.from và flatMap để lấy tất cả inputs
    // const allInputsFlatMap = Array.from(elementsNumber).flatMap(element => 
    //     Array.from(element.querySelectorAll('.ant-input-number-input'))
    // );
    // console.log('Input elements (flatMap):', allInputsFlatMap);
    
    // Cách 4: Tìm input có giá trị cụ thể (ví dụ: tìm input có value > 0)
    // const inputsWithValue = Array.from(elementsNumber).flatMap(element => {
    //     const inputs = element.querySelectorAll('.ant-input-number-input');
    //     return Array.from(inputs).filter(input => {
    //         const value = parseFloat(input.value);
    //         return !isNaN(value) && value > 0;
    //     });
    // });
    
    // Hiển thị thông báo trên trang web
    // const notification = document.createElement('div');
    // notification.style.cssText = `
    //     position: fixed;
    //     top: 20px;
    //     right: 20px;
    //     background: #4CAF50;
    //     color: white;
    //     padding: 15px;
    //     border-radius: 5px;
    //     z-index: 10000;
    //     font-family: Arial, sans-serif;
    //     box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    // `;
    // notification.textContent = `Đã tìm thấy ${elementsWithBothClasses.length} elements có cả 2 class price-info và currency`;
    // document.body.appendChild(notification);
    
    // // Tự động xóa thông báo sau 3 giây
    // setTimeout(() => {
    //     if (notification.parentNode) {
    //         notification.parentNode.removeChild(notification);
    //     }
    // }, 3000);
});

// document.getElementById('btn2').addEventListener('click', () => {
//     console.log('Nút 2 được click');
//     // Thêm xử lý cho nút 2 ở đây
// }); 