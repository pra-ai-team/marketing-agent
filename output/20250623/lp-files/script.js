/**
 * ===========================================
 * 和光葬儀社 ランディングページ JavaScript
 * 作成日: 2025年6月23日
 * 目的: ユーザビリティ向上・コンバージョン追跡
 * ===========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('和光葬儀社 LP JavaScript 読み込み完了');
    
    // 初期化関数を順次実行
    initFAQAccordion();
    initSmoothScroll();
    initFormHandling();
    initPhoneTracking();
    initScrollAnimations();
    initMobileOptimization();
    initAnalyticsTracking();
    
    console.log('全ての機能が初期化されました');
});

/**
 * FAQアコーディオン機能
 * よくある質問セクションの開閉機能
 */
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        if (question) {
            question.addEventListener('click', function() {
                const isActive = item.classList.contains('active');
                
                // 他のFAQを閉じる
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });
                
                // クリックされたFAQを開く（既に開いている場合は閉じる）
                if (!isActive) {
                    item.classList.add('active');
                    
                    // アナリティクス追跡
                    trackEvent('FAQ', 'open', question.textContent.trim());
                }
            });
        }
    });
    
    console.log('FAQ アコーディオン機能を初期化しました');
}

/**
 * スムーススクロール機能
 * アンカーリンクのスムーズなスクロール
 */
function initSmoothScroll() {
    const anchors = document.querySelectorAll('a[href^="#"]');
    
    anchors.forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = 80; // ヘッダーの高さ
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // アナリティクス追跡
                trackEvent('Navigation', 'scroll', targetId);
            }
        });
    });
    
    console.log('スムーススクロール機能を初期化しました');
}

/**
 * フォーム送信処理
 * お問い合わせフォームのバリデーションと送信
 */
function initFormHandling() {
    const form = document.getElementById('contactForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // フォームデータ取得
            const formData = new FormData(this);
            const name = formData.get('name')?.trim();
            const phone = formData.get('phone')?.trim();
            const urgency = formData.get('urgency');
            const email = formData.get('email')?.trim();
            const message = formData.get('message')?.trim();
            
            // バリデーション
            if (!validateForm(name, phone, urgency)) {
                return;
            }
            
            // 送信処理
            submitContactForm({
                name,
                phone,
                urgency,
                email,
                message
            });
        });
    }
    
    console.log('フォーム送信処理を初期化しました');
}

/**
 * フォームバリデーション
 */
function validateForm(name, phone, urgency) {
    // 必須項目チェック
    if (!name || !phone || !urgency) {
        showAlert('error', 'お名前、電話番号、緊急度は必須項目です。');
        return false;
    }
    
    // 名前の長さチェック
    if (name.length < 2) {
        showAlert('error', 'お名前は2文字以上で入力してください。');
        return false;
    }
    
    // 電話番号の形式チェック
    const phonePattern = /^[\d\-\+\(\)\s]{10,15}$/;
    if (!phonePattern.test(phone)) {
        showAlert('error', '正しい電話番号を入力してください。（10-15桁）');
        return false;
    }
    
    return true;
}

/**
 * フォーム送信実行
 */
function submitContactForm(data) {
    const submitButton = document.querySelector('#contactForm button[type="submit"]');
    const originalText = submitButton.textContent;
    
    // ローディング状態
    submitButton.textContent = '送信中...';
    submitButton.disabled = true;
    
    // 緊急度に応じた処理
    const isUrgent = data.urgency === '今すぐ';
    const processingTime = isUrgent ? 1000 : 2000;
    
    // 送信シミュレーション（実際の実装では適切なAPIエンドポイントに送信）
    setTimeout(() => {
        // 成功処理
        if (isUrgent) {
            showAlert('success', 'お急ぎの件承りました。\n5分以内に担当者よりお電話いたします。');
        } else {
            showAlert('success', 'お問い合わせありがとうございます。\n24時間以内に担当者よりご連絡いたします。');
        }
        
        // フォームリセット
        document.getElementById('contactForm').reset();
        
        // ボタンを元に戻す
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        
        // コンバージョン追跡
        trackConversion('form_submit', data.urgency);
        
    }, processingTime);
}

/**
 * アラート表示
 */
function showAlert(type, message) {
    // 既存のアラートを削除
    const existingAlert = document.querySelector('.custom-alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // アラート要素作成
    const alert = document.createElement('div');
    alert.className = `custom-alert custom-alert-${type}`;
    alert.innerHTML = `
        <div class="alert-content">
            <div class="alert-icon">${type === 'success' ? '✓' : '⚠'}</div>
            <div class="alert-message">${message.replace(/\n/g, '<br>')}</div>
            <button class="alert-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    // スタイル設定
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(alert);
    
    // 自動消去
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

/**
 * 電話番号クリック追跡
 */
function initPhoneTracking() {
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    
    phoneLinks.forEach(link => {
        link.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('href').replace('tel:', '');
            
            // アナリティクス追跡
            trackEvent('Contact', 'phone_click', phoneNumber);
            
            // 緊急性の高いアクションとして記録
            trackConversion('phone_click', 'urgent');
            
            console.log('電話クリック追跡:', phoneNumber);
        });
    });
    
    console.log('電話クリック追跡を初期化しました');
}

/**
 * スクロールアニメーション
 * 要素が表示されたときのアニメーション
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // セクション表示の追跡
                const sectionName = entry.target.querySelector('.section-title')?.textContent || 
                                   entry.target.className;
                trackEvent('Engagement', 'section_view', sectionName);
            }
        });
    }, observerOptions);
    
    // 監視対象要素
    const sections = document.querySelectorAll('section, .hero');
    sections.forEach(section => observer.observe(section));
    
    console.log('スクロールアニメーションを初期化しました');
}

/**
 * モバイル最適化
 */
function initMobileOptimization() {
    // モバイル電話ボタンの表示制御
    const mobilePhoneBtn = document.querySelector('.mobile-phone-fixed');
    
    if (window.innerWidth <= 768 && mobilePhoneBtn) {
        mobilePhoneBtn.style.display = 'block';
    }
    
    // リサイズ対応
    window.addEventListener('resize', debounce(() => {
        if (mobilePhoneBtn) {
            mobilePhoneBtn.style.display = window.innerWidth <= 768 ? 'block' : 'none';
        }
    }, 250));
    
    // タッチデバイス対応
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
    }
    
    console.log('モバイル最適化を初期化しました');
}

/**
 * アナリティクス追跡
 */
function initAnalyticsTracking() {
    // ページ滞在時間追跡
    let startTime = Date.now();
    let engagementTracked = false;
    
    // 30秒滞在でエンゲージメント追跡
    setTimeout(() => {
        if (!engagementTracked) {
            trackEvent('Engagement', 'time_on_page', '30_seconds');
            engagementTracked = true;
        }
    }, 30000);
    
    // ページ離脱時
    window.addEventListener('beforeunload', () => {
        const timeOnPage = Math.round((Date.now() - startTime) / 1000);
        trackEvent('Engagement', 'time_on_page_total', timeOnPage.toString());
    });
    
    // スクロール深度追跡
    let maxScroll = 0;
    window.addEventListener('scroll', throttle(() => {
        const scrollPercent = Math.round(
            (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
        );
        
        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;
            
            // 25%, 50%, 75%, 100%でイベント送信
            if ([25, 50, 75, 100].includes(scrollPercent)) {
                trackEvent('Engagement', 'scroll_depth', `${scrollPercent}%`);
            }
        }
    }, 1000));
    
    console.log('アナリティクス追跡を初期化しました');
}

/**
 * イベント追跡（Google Analytics）
 */
function trackEvent(category, action, label = '') {
    // Google Analytics 4
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            event_category: category,
            event_label: label,
            custom_parameter_1: 'wako_sougisya_lp'
        });
    }
    
    // データレイヤー
    if (typeof dataLayer !== 'undefined') {
        dataLayer.push({
            event: 'custom_event',
            event_category: category,
            event_action: action,
            event_label: label,
            page_type: 'landing_page',
            company: 'wako_sougisya'
        });
    }
    
    console.log(`イベント追跡: ${category} > ${action} > ${label}`);
}

/**
 * コンバージョン追跡
 */
function trackConversion(type, value = '') {
    // Google Analytics コンバージョン
    if (typeof gtag !== 'undefined') {
        gtag('event', 'conversion', {
            send_to: 'AW-XXXXXXXXX/XXXXXXXX', // 実際のコンバージョンIDに置き換え
            value: type === 'phone_click' ? 50 : 100,
            currency: 'JPY',
            conversion_type: type,
            conversion_value: value
        });
    }
    
    // カスタムコンバージョン追跡
    trackEvent('Conversion', type, value);
    
    console.log(`コンバージョン追跡: ${type} - ${value}`);
}

/**
 * ユーティリティ関数
 */

// スロットル関数（イベント実行頻度制限）
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
    }
}

// デバウンス関数（イベント実行遅延）
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 緊急時対応機能
 * 24時間対応を強調する機能
 */
function initEmergencyFeatures() {
    // 現在時刻表示
    function updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ja-JP', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const timeElements = document.querySelectorAll('.current-time');
        timeElements.forEach(element => {
            element.textContent = timeString;
        });
    }
    
    // 1分ごとに時刻更新
    updateCurrentTime();
    setInterval(updateCurrentTime, 60000);
    
    // 緊急時メッセージの表示
    const currentHour = new Date().getHours();
    if (currentHour < 6 || currentHour > 22) {
        const emergencyMessages = document.querySelectorAll('.emergency-message');
        emergencyMessages.forEach(element => {
            element.style.display = 'block';
            element.textContent = '深夜・早朝でも専門スタッフが対応いたします';
        });
    }
}

// 緊急時機能も初期化
document.addEventListener('DOMContentLoaded', function() {
    initEmergencyFeatures();
});

/**
 * エラーハンドリング
 */
window.addEventListener('error', function(e) {
    console.error('JavaScript エラー:', e.error);
    
    // 重要でないエラーの場合は続行
    if (e.error && e.error.name !== 'TypeError') {
        trackEvent('Error', 'javascript_error', e.error.message);
    }
});

/**
 * パフォーマンス監視
 */
window.addEventListener('load', function() {
    // ページ読み込み時間の測定
    setTimeout(() => {
        if (window.performance) {
            const loadTime = window.performance.timing.loadEventEnd - 
                           window.performance.timing.navigationStart;
            
            if (loadTime > 0) {
                trackEvent('Performance', 'page_load_time', Math.round(loadTime / 1000).toString());
            }
        }
    }, 0);
});

console.log('和光葬儀社 LP JavaScript 全機能読み込み完了');
