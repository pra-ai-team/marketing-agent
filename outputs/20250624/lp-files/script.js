// DOMが読み込まれた後に実行
document.addEventListener('DOMContentLoaded', function() {
    
    // スムーススクロール機能
    initSmoothScroll();
    
    // フォーム機能
    initContactForm();
    
    // スクロールアニメーション
    initScrollAnimations();
    
    // ヘッダーの表示制御
    initHeaderControl();
    
    // 電話タップ追跡
    initPhoneTracking();
    
    // FAQアコーディオン機能
    initFAQAccordion();
});

// スムーススクロール機能
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// お問い合わせフォーム機能
function initContactForm() {
    const form = document.getElementById('contact-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // バリデーション
            const name = document.getElementById('name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const inquiryType = document.getElementById('inquiry-type').value;
            
            if (!name || !phone || !inquiryType) {
                alert('必須項目を入力してください。');
                return;
            }
            
            // 成功メッセージ表示
            alert('お問い合わせありがとうございます。24時間以内にご連絡いたします。');
            form.reset();
        });
        
        // リアルタイムバリデーション
        const inputs = form.querySelectorAll('input[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearErrorMessage(this);
            });
        });
    }
}

// フォームバリデーション
function validateForm() {
    let isValid = true;
    
    // 必須フィールドのチェック
    const name = document.getElementById('name');
    const phone = document.getElementById('phone');
    const inquiryType = document.getElementById('inquiry-type');
    
    if (!validateField(name)) isValid = false;
    if (!validateField(phone)) isValid = false;
    if (!validateField(inquiryType)) isValid = false;
    
    // メールアドレスのフォーマットチェック（任意フィールド）
    const email = document.getElementById('email');
    if (email && email.value && !validateEmail(email.value)) {
        showErrorMessage(email, 'メールアドレスの形式が正しくありません');
        isValid = false;
    }
    
    return isValid;
}

// 個別フィールドのバリデーション
function validateField(field) {
    const value = field.value.trim();
    
    if (field.hasAttribute('required') && !value) {
        showErrorMessage(field, 'この項目は必須です');
        return false;
    }
    
    if (field.type === 'tel' && value) {
        if (!validatePhone(value)) {
            showErrorMessage(field, '電話番号の形式が正しくありません');
            return false;
        }
    }
    
    clearErrorMessage(field);
    return true;
}

// 電話番号のバリデーション
function validatePhone(phone) {
    const phoneRegex = /^[\d\-\+\(\)\s]{10,}$/;
    return phoneRegex.test(phone);
}

// メールアドレスのバリデーション
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// エラーメッセージの表示
function showErrorMessage(field, message) {
    clearErrorMessage(field);
    
    const errorSpan = document.createElement('span');
    errorSpan.className = 'error-message';
    errorSpan.textContent = message;
    errorSpan.style.color = '#ef4444';
    errorSpan.style.fontSize = '0.8em';
    errorSpan.style.marginTop = '5px';
    errorSpan.style.display = 'block';
    
    field.style.borderColor = '#ef4444';
    field.parentNode.appendChild(errorSpan);
}

// エラーメッセージのクリア
function clearErrorMessage(field) {
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    field.style.borderColor = '#e5e7eb';
}

// 成功メッセージの表示
function showSuccessMessage() {
    const message = document.createElement('div');
    message.innerHTML = `
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            z-index: 10000;
            text-align: center;
            max-width: 400px;
            width: 90%;
        ">
            <div style="font-size: 3em; margin-bottom: 20px;">✓</div>
            <h3 style="margin-bottom: 15px; color: #1e3a8a;">送信完了</h3>
            <p style="margin-bottom: 20px; color: #6b7280;">
                お問い合わせありがとうございます。<br>
                担当者より24時間以内にご連絡いたします。
            </p>
            <button onclick="this.parentElement.parentElement.remove()" style="
                background: #1e3a8a;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
            ">閉じる</button>
        </div>
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
        " onclick="this.parentElement.remove()"></div>
    `;
    
    document.body.appendChild(message);
    
    // 3秒後に自動で閉じる
    setTimeout(() => {
        if (message.parentNode) {
            message.remove();
        }
    }, 3000);
}

// スクロールアニメーション
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // アニメーション対象要素の設定
    const animateElements = document.querySelectorAll('.stat-item, .review-card, .support-feature');
    
    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
    
    // 数値カウントアニメーション
    initCounterAnimation();
}

// 数値カウントアニメーション
function initCounterAnimation() {
    const counters = document.querySelectorAll('.stat-number');
    
    const observerOptions = {
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.textContent.replace(/\D/g, ''));
                const suffix = counter.textContent.replace(/[\d]/g, '');
                
                animateCounter(counter, target, suffix);
                observer.unobserve(counter);
            }
        });
    }, observerOptions);
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// カウンターアニメーション関数
function animateCounter(element, target, suffix) {
    let current = 0;
    const increment = target / 60; // 1秒間で60フレーム
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        element.textContent = Math.floor(current) + suffix;
    }, 16); // 16ms ≈ 60fps
}

// ヘッダーの表示制御
function initHeaderControl() {
    let lastScrollTop = 0;
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // 下スクロール時はヘッダーを隠す
            header.style.transform = 'translateY(-100%)';
        } else {
            // 上スクロール時はヘッダーを表示
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // ヘッダーにトランジション効果を追加
    header.style.transition = 'transform 0.3s ease';
}

// 電話タップ追跡
function initPhoneTracking() {
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    
    phoneLinks.forEach(link => {
        link.addEventListener('click', function() {
            // アナリティクス用のイベント送信
            console.log('電話番号クリック:', this.href);
        });
    });
}

// ページの読み込み完了時の処理
window.addEventListener('load', function() {
    // ローディングアニメーションなどがあれば、ここで処理
    
    // Core Web Vitals の測定（パフォーマンス監視）
    if ('performance' in window && 'measure' in performance) {
        // LCP (Largest Contentful Paint) の測定
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1];
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'LCP', {
                    'event_category': 'Web Vitals',
                    'value': Math.round(lastEntry.startTime),
                    'non_interaction': true,
                });
            }
        }).observe({entryTypes: ['largest-contentful-paint']});
        
        // FID (First Input Delay) の測定
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            entries.forEach((entry) => {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'FID', {
                        'event_category': 'Web Vitals',
                        'value': Math.round(entry.processingStart - entry.startTime),
                        'non_interaction': true,
                    });
                }
            });
        }).observe({entryTypes: ['first-input']});
    }
});

// スクロール深度の測定
let maxScrollDepth = 0;

window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = Math.round((scrollTop / docHeight) * 100);
    
    if (scrollPercent > maxScrollDepth) {
        maxScrollDepth = scrollPercent;
        
        // 25%, 50%, 75%, 100% の節目で Google Analytics に送信
        if ([25, 50, 75, 100].includes(scrollPercent)) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'scroll', {
                    'event_category': 'engagement',
                    'event_label': `${scrollPercent}%`,
                    'value': scrollPercent
                });
            }
        }
    }
});

// ユーザビリティ向上のための機能

// フォーカス可能な要素のアウトライン改善
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// CSSでキーボードナビゲーション時のアウトラインを設定
const style = document.createElement('style');
style.textContent = `
    .keyboard-navigation *:focus {
        outline: 2px solid #1e3a8a !important;
        outline-offset: 2px !important;
    }
    
    :not(.keyboard-navigation) *:focus {
        outline: none !important;
    }
`;
document.head.appendChild(style);

// エラーハンドリング
window.addEventListener('error', function(e) {
    // エラーログをGoogle Analyticsに送信（本番環境での監視用）
    if (typeof gtag !== 'undefined') {
        gtag('event', 'javascript_error', {
            'event_category': 'error',
            'event_label': e.message,
            'non_interaction': true,
        });
    }
});

// 外部リンクのトラッキング
document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    
    if (link && link.hostname !== window.location.hostname) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'outbound_link', {
                'event_category': 'engagement',
                'event_label': link.href,
                'transport_type': 'beacon'
            });
        }
    }
});

// ページ表示時のスクロール位置復元を防ぐ
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}

// タッチデバイス対応
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}

// FAQアコーディオン機能
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', function() {
            const isActive = item.classList.contains('active');
            
            // 他のFAQアイテムを閉じる
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // クリックしたアイテムの開閉を切り替え
            if (isActive) {
                item.classList.remove('active');
            } else {
                item.classList.add('active');
            }
        });
    });
} 