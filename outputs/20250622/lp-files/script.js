// ====================
// 和光葬儀社 LP JavaScript
// ====================

document.addEventListener('DOMContentLoaded', function() {
    
    // ====================
    // FAQアコーディオン機能
    // ====================
    function initFAQ() {
        const faqItems = document.querySelectorAll('.faq-item');
        
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            
            question.addEventListener('click', () => {
                // 現在のアイテムがアクティブかチェック
                const isActive = item.classList.contains('active');
                
                // すべてのFAQアイテムを閉じる
                faqItems.forEach(faqItem => {
                    faqItem.classList.remove('active');
                });
                
                // クリックされたアイテムがアクティブでなければ開く
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        });
    }
    
    // ====================
    // スムーススクロール
    // ====================
    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    const headerOffset = 80; // ヘッダーの高さ分オフセット
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // ====================
    // 電話番号クリック追跡
    // ====================
    function initPhoneTracking() {
        const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
        
        phoneLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Google Analytics イベント送信
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'phone_click', {
                        event_category: 'Contact',
                        event_label: 'Phone Call',
                        value: 1
                    });
                }
                
                // カスタムイベント送信（他の分析ツール用）
                if (typeof dataLayer !== 'undefined') {
                    dataLayer.push({
                        event: 'phone_click',
                        phone_number: this.getAttribute('href').replace('tel:', '')
                    });
                }
                
                console.log('Phone click tracked:', this.getAttribute('href'));
            });
        });
    }
    
    // ====================
    // フォーム送信処理
    // ====================
    function initFormHandling() {
        const form = document.querySelector('.contact-form .form');
        
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // フォームデータ取得
                const formData = new FormData(this);
                const name = formData.get('name');
                const phone = formData.get('phone');
                const message = formData.get('message');
                
                // バリデーション
                if (!name || !phone) {
                    alert('お名前とお電話番号は必須項目です。');
                    return;
                }
                
                // 電話番号の簡易バリデーション
                const phonePattern = /^[\d\-\+\(\)\s]+$/;
                if (!phonePattern.test(phone)) {
                    alert('正しい電話番号を入力してください。');
                    return;
                }
                
                // Google Analytics コンバージョン追跡
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'form_submit', {
                        event_category: 'Contact',
                        event_label: 'Form Submission',
                        value: 1
                    });
                }
                
                // フォーム送信処理（実際の実装では適切なエンドポイントに送信）
                submitForm(formData);
            });
        }
    }
    
    // ====================
    // フォーム送信API（実装例）
    // ====================
    function submitForm(formData) {
        // ローディング表示
        const submitButton = document.querySelector('.contact-form button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = '送信中...';
        submitButton.disabled = true;
        
        // 実際の実装ではここでAPIにデータを送信
        // fetch('/api/contact', {
        //     method: 'POST',
        //     body: formData
        // })
        
        // デモ用の遅延処理
        setTimeout(() => {
            alert('お問い合わせありがとうございます。\n担当者より24時間以内にご連絡いたします。');
            
            // フォームリセット
            document.querySelector('.contact-form .form').reset();
            
            // ボタンを元に戻す
            submitButton.textContent = originalText;
            submitButton.disabled = false;
            
            // Google Analytics コンバージョン完了追跡
            if (typeof gtag !== 'undefined') {
                gtag('event', 'conversion', {
                    send_to: 'AW-CONVERSION_ID/CONVERSION_LABEL',
                    value: 1.0,
                    currency: 'JPY'
                });
            }
            
        }, 2000);
    }
    
    // ====================
    // スクロール追跡
    // ====================
    function initScrollTracking() {
        let scrollTracked = {
            '25%': false,
            '50%': false,
            '75%': false,
            '100%': false
        };
        
        window.addEventListener('scroll', throttle(() => {
            const scrollPercent = Math.round(
                (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
            );
            
            // スクロール率の追跡
            Object.keys(scrollTracked).forEach(percentage => {
                const percent = parseInt(percentage);
                if (scrollPercent >= percent && !scrollTracked[percentage]) {
                    scrollTracked[percentage] = true;
                    
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'scroll', {
                            event_category: 'Engagement',
                            event_label: `Scroll ${percentage}`,
                            value: percent
                        });
                    }
                }
            });
        }, 1000));
    }
    
    // ====================
    // CTAボタンクリック追跡
    // ====================
    function initCTATracking() {
        const ctaButtons = document.querySelectorAll('.btn-primary, .btn-secondary');
        
        ctaButtons.forEach((button, index) => {
            button.addEventListener('click', function() {
                const buttonText = this.textContent.trim();
                const section = this.closest('section')?.className || 'unknown';
                
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'cta_click', {
                        event_category: 'CTA',
                        event_label: buttonText,
                        custom_parameter_1: section,
                        value: 1
                    });
                }
                
                console.log('CTA clicked:', buttonText, 'in section:', section);
            });
        });
    }
    
    // ====================
    // ページ滞在時間追跡
    // ====================
    function initTimeTracking() {
        const startTime = Date.now();
        
        // ページ離脱時の滞在時間を記録
        window.addEventListener('beforeunload', () => {
            const timeSpent = Math.round((Date.now() - startTime) / 1000);
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'timing_complete', {
                    name: 'page_view_time',
                    value: timeSpent
                });
            }
        });
        
        // 一定時間経過での中間記録
        const timeCheckpoints = [30, 60, 120, 300]; // 30秒、1分、2分、5分
        
        timeCheckpoints.forEach(seconds => {
            setTimeout(() => {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'timing_milestone', {
                        event_category: 'Engagement',
                        event_label: `${seconds}s_engaged`,
                        value: seconds
                    });
                }
            }, seconds * 1000);
        });
    }
    
    // ====================
    // セクション表示追跡
    // ====================
    function initSectionTracking() {
        const sections = document.querySelectorAll('section[id]');
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.id;
                    
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'section_view', {
                            event_category: 'Navigation',
                            event_label: sectionId,
                            value: 1
                        });
                    }
                    
                    console.log('Section viewed:', sectionId);
                }
            });
        }, observerOptions);
        
        sections.forEach(section => {
            observer.observe(section);
        });
    }
    
    // ====================
    // ユーティリティ関数
    // ====================
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    // ====================
    // 初期化処理
    // ====================
    function init() {
        console.log('和光葬儀社 LP JavaScript initialized');
        
        // 各機能の初期化
        initFAQ();
        initSmoothScroll();
        initPhoneTracking();
        initFormHandling();
        initScrollTracking();
        initCTATracking();
        initTimeTracking();
        initSectionTracking();
    }
    
    // 初期化実行
    init();
    
    // ====================
    // Google Analytics 設定例
    // ====================
    /*
    // Google Analytics の設定は head タグ内で行うか、
    // Google Tag Manager を使用することを推奨
    
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID', {
        // カスタム設定
        send_page_view: true,
        custom_map: {
            'custom_parameter_1': 'section'
        }
    });
    */
});

// ====================
// エラーハンドリング
// ====================
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    
    // エラー追跡（オプション）
    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            description: e.error.toString(),
            fatal: false
        });
    }
});

// ====================
// パフォーマンス監視
// ====================
window.addEventListener('load', function() {
    // ページ読み込み完了時の処理
    if (typeof gtag !== 'undefined') {
        gtag('event', 'page_load_complete', {
            event_category: 'Performance',
            value: Date.now()
        });
    }
    
    // Core Web Vitals の測定（Web Vitals ライブラリが必要）
    /*
    if (typeof webVitals !== 'undefined') {
        webVitals.getCLS(console.log);
        webVitals.getFID(console.log);
        webVitals.getFCP(console.log);
        webVitals.getLCP(console.log);
        webVitals.getTTFB(console.log);
    }
    */
});

// ====================
// 開発用デバッグ機能
// ====================
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('Development mode detected - Debug logging enabled');
    
    // 開発環境でのみ実行されるデバッグコード
    window.debugLP = {
        trackEvent: function(event, data) {
            console.log('Debug Event:', event, data);
        },
        getAnalyticsData: function() {
            return {
                pageViews: 'Debug data',
                conversions: 'Debug data',
                phoneClicks: 'Debug data'
            };
        }
    };
} 